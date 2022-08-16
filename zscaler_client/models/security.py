from .base import BaseModel

class AdvancedSecurityBlacklist(BaseModel):

    endpoint = '/security/advanced/blacklistUrls'
    actions = []

    def update(self):
        raise NotImplementedError

    def save(self):
        raise NotImplementedError
    
    def search(self):
        raise NotImplementedError

    def add_to_list(self, urls: list = []) -> bool:
        '''
        Adds a url or multiple urls to the built in Deny List under Advanced Threat Protection
        '''

        request_body = {
            'blacklistUrls': urls
        }

        if len(urls) > 0:
            response = self.api_client.call_api(method='POST', endpoint='/security/advanced/blacklistUrls?action=ADD_TO_LIST', json=request_body)
            if response.status_code in [200,204]:
                return True
        
        return False

    def remove_from_list(self, urls: list = []) -> bool:
        '''
        Removes a url or multiple urls from the built in Deny List under Advanced Threat Protection
        Returns: True|False
        '''

        request_body = {
            'blacklistUrls': urls
        }

        if len(urls) > 0:
            response = self.api_client.call_api(method='POST', endpoint='/security/advanced/blacklistUrls?action=REMOVE_FROM_LIST', json=request_body)
            if response.status_code in [200,204]:
                return True
        
        return False