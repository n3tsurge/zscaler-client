from .base import BaseModel
from ..client import get_client

class UrlClassificationInformation(BaseModel):

    endpoint = "/urlLookup"

    @classmethod
    def search(cls, url: list = [], **kwargs):
        '''
        Performs search operations on a model
        '''
        if not hasattr(cls, 'api_client'):
            cls.api_client = get_client()

        api_params = {}

        if 'params' in kwargs:
            api_params['params'] = kwargs.get('params', {})

        response = cls.api_client.call_api(method='POST', endpoint=cls.endpoint, json=url, **api_params)
        return [cls(**r) for r in response.json() if r]


class UrlCategory(BaseModel):

    endpoint = "/urlCategories"
    updatable_fields = [
        'id','configuredName', 'keywords', 'keywordsRetainingParentCategory', 'urls',
        'dbCategorizedUrls', 'ipRanges', 'ipRangesRetainingParentCategory', 'customCategory',
        'scopes', 'editable', 'description'
    ]
    actions = []
