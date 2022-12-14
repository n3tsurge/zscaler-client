import time
import logging
from .errors import *
from requests import Session

class APIClient:

    def __init__(self, config, base_url, *args, **kwargs):

        self.config = config
        self.session = Session()
        self.base_url = base_url
        self.scheme =  kwargs.get('scheme','https')

        # Configure logging 
        log_level = kwargs.get('log_level', 'INFO')
        log_levels = {
            'DEBUG': logging.DEBUG,
            'ERROR': logging.ERROR,
            'INFO': logging.INFO
        }
        
        log_handler = logging.StreamHandler()
        log_handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.addHandler(log_handler)
        self.logger.setLevel(log_levels[log_level])
        self.log_level = log_level


    def obfuscate_api_key(self, now) -> str:
        '''
        Obfuscates the ZScaler API key per https://help.zscaler.com/zia/getting-started-zia-api
        '''

        seed = self.config['api_key']
        n = str(now)[-6:]
        r = str(int(n) >> 1).zfill(6)
        key = ""
        for i in range(0, len(str(n)), 1):
            key += seed[int(str(n)[i])]
        for j in range(0, len(str(r)), 1):
            key += seed[int(str(r)[j])+2]

        return key


    def call_api(self, method: str = "GET", endpoint: str = "", json: dict = {}, data: dict = {}):
        '''
        Makes a call to the API using the existing APIClient session
        '''

        request_map = {
            'GET': self.session.get,
            'POST': self.session.post,
            'DELETE': self.session.delete,
            'PUT': self.session.put
        }

        request = request_map[method]

        request_parameters = {}

        if json:
            request_parameters['json'] = json

        if data:
            request_parameters['data'] = data

        self.logger.info(f"Making request to {endpoint}")

        response = request(f"{self.scheme}://{self.base_url}{endpoint}", **request_parameters)
        if response.status_code in [200, 204, 409]:
            return response
        else:
            raise RequestError(response.text)


    def auth(self, username, password):
        '''
        Authenticates to the ZScaler API, which if successful with update the APIClient session
        with a JSESSIONID cookie that will be used in all future requests
        '''

        self.session.headers.update({'Content-Type': 'application/json'})

        now = int(time.time() * 1000)

        request_body = {
            'apiKey': self.obfuscate_api_key(now),
            'username': username,
            'password': password,
            'timestamp': now
        }

        response = self.call_api(method='POST', endpoint="/api/v1/authenticatedSession", json=request_body)


    def activate(self, retry_time: int = 1, max_retries: int = 5):
        '''
        Activate the pending configuration, when a 409 request is returned, wait retry_time
        and try again until max_retries is reached and raise an error
        '''

        retries = 0
        activation_success = False

        while not activation_success and retries != max_retries:
            response = self.call_api(method='POST', endpoint="/api/v1/status/activate")
            if response.status_code == 409:
                retries += 1
                time.sleep(1)
            else:
                activation_success = True

        if retries == max_retries:
            ActivationError(f"Attempted to activate configuration but failed after {max_retries} attempts")


    def logout(self):
        '''
        Kills the active session to the API
        '''

        response = self.call_api(method='DELETE', endpoint="/api/v1/authenticatedSesssion")


    def url_lookup(self, url: list = []):
        '''
        Calls the /api/v1/urlLookup endpoint with a list of URLs and returns
        the categories for each URL
        '''

        response = self.call_api(method='POST', endpoint="/api/v1/urlLookup", json=['google.com'])
        if response.status_code == 200:
            return response.json()


    def list_groups(self):
        '''
        Returns a list of all the groups in the Zscaler platform
        '''

        response = self.call_api(endpoint="/api/v1/groups")
        return response.json()


    def get_group_users(self, group_name, group=True):
        '''
        Returns a list of users in a specific group
        '''

        group_or_dept = "group" if group else "dept"

        response = self.call_api(endpoint=f"/api/v1/users?{group_or_dept}={group_name}")
        return response.json()
        

    def get_dept_users(self, dept_name):
        '''
        Returns a list of users in a specific department
        '''
        return self.get_group_users(dept_name, group=False)


    def add_to_denylist(self, values: list = []):
        '''
        Adds a value or multiple values to the built in Deny List under Advanced Threat Protection
        '''

        request_body = {
            'blacklistUrls': values
        }

        if len(values) > 0:
            response = self.call_api(method='POST', endpoint='/api/v1/security/advanced/blacklistUrls?action=ADD_TO_LIST', json=request_body)
            return response

        return None

    
    def add_to_denylist(self, values: list = []):
        '''
        Removes a value or multiple values from the built in Deny List under Advanced Threat Protection
        '''

        request_body = {
            'blacklistUrls': values
        }

        if len(values) > 0:
            response = self.call_api(method='POST', endpoint='/api/v1/security/advanced/blacklistUrls?action=REMOVE_FROM_LIST', json=request_body)
            return response

        return None


    def create_vpn_credentials(self, cred_type: str = "CN", fqdn: str = None, preSharedKey: str = None, location: dict = None, generate_psk: bool = False, comments: str = ""):
        '''
        Creates new VPN credentials
        '''

        request_body = {
            'type': cred_type,
            'comments': comments
        }

        if cred_type not in ['CN','IP','UFQDN','XAUTH']:
            raise CredentialError('Invalid credential type.  Must be one of CN, IP, UFQDN, XAUTH')

        if cred_type in ['UFQDN', 'IP'] and not (preSharedKey or generate_psk):
            raise CredentialError('A pre-shared key is required when using an UFQDN or IP credential type')
        else:
            if generate_psk and not preSharedKey:
                pass
            else:
                self.logger.info('Skipping PSK generation as one was supplied')

            request_body['preSharedKey'] = preSharedKey

        if cred_type in ['UFQDN', 'XAUTH'] and not fqdn:
            raise CredentialError('An fqdn is required when using an UFQDN or XAUTH credential type')
        else:
            request_body['fqdn'] = fqdn

        if location != {}:
            request_body['location'] = location

        response = self.call_api(endpoint=f"/api/v1/vpnCredentials", method="POST", json=request_body)
        return response

