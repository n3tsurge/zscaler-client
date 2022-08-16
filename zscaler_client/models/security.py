from .base import BaseModel

class AdvancedSecurityBlacklist(BaseModel):

    endpoint = '/security/advanced/blacklistUrls'
    actions = []

    @classmethod
    def add_to_list(cls, urls: list = []) -> bool:
        '''
        Adds a url or multiple urls to the built in Deny List under Advanced Threat Protection
        '''

        cls.get_client()

        request_body = {
            'blacklistUrls': urls
        }

        if len(urls) > 0:
            response = cls.api_client.call_api(method='POST', endpoint=f'{cls.endpoint}?action=ADD_TO_LIST', json=request_body)
            if response.status_code in [200,204]:
                return True
        
        return False

    @classmethod
    def remove_from_list(cls, urls: list = []) -> bool:
        '''
        Removes a url or multiple urls from the built in Deny List under Advanced Threat Protection
        Returns: True|False
        '''

        cls.get_client()

        request_body = {
            'blacklistUrls': urls
        }

        if len(urls) > 0:
            response = cls.api_client.call_api(method='POST', endpoint=f'{cls.endpoint}?action=REMOVE_FROM_LIST', json=request_body)
            if response.status_code in [200,204]:
                return True
        
        return False