import json
from json import JSONEncoder
from ..errors import *
from ..client import get_client


class CustomJsonEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, JSONSerializable):
            return {k: o.__dict__[k] for k in o.__dict__ if k != 'api_client'}
        return json.JSONEncoder.default(self, o)


class JSONSerializable(object):
    ''' Allows for an object to be represented in JSON format '''

    def jsonify(self):
        ''' Returns a json string of the object '''
        
        return json.dumps(self, sort_keys=True, indent=4, cls=CustomJsonEncoder)

    def attr(self, attributes, name, default, error=None):
        ''' Fetches an attribute from the passed dictionary '''
        
        is_required = error is not None

        if is_required and name not in attributes:
            raise ValueError(error)
        else:
            return attributes.get(name, default)


class BaseModel(JSONSerializable):
    '''
    A BaseModel used by all other Models
    '''

    def __init__(self, client_alias='default', *args, **kwargs):

        # The API client used to make API calls
        self.api_client = get_client()
        self.internal_fields = ['api_client', 'actions', 'updatable_fields']

        if (kwargs):
            for k in kwargs:
                self.__dict__[k] = kwargs.get(k, None)


    def update(self, **kwargs):
        '''
        Updates the model using the fields modified, used when updating a single field
        e.g. model.update(name="foo")
        '''

        if 'update' not in self.actions:
            raise NotImplementedError(f'The "update" action is not implemented on {self.__class__.__name__}')

        request_body = {}

        if kwargs:
            for k in kwargs:
                if k in self.updatable_fields:
                    request_body[k] = kwargs[k]

        if request_body != {}:
            self.api_client.call_api(method='PUT', endpoint=f'{self.endpoint}/{self.id}', json=request_body)


    def save(self):
        '''
        Saves the entire model used when using model.field = "x" then running model.save()
        '''

        if 'save' not in self.actions:
            raise NotImplementedError(f'The "save" action is not implemented on {self.__class__.__name__}')

        request_body = {k: self.__dict__[k] for k in self.__dict__ if k in self.updatable_fields}
        if len(request_body) > 0:
            if not new:
                response = self.api_client.call_api(method='PUT', endpoint=f'{self.endpoint}/{self.id}', json=request_body)
                return response
        
        return None


    @classmethod
    def search(cls, **kwargs):
        '''
        Performs search operations on a model
        '''
        if not hasattr(cls, 'api_client'):
            cls.api_client = get_client()

        api_params = {}

        if 'params' in kwargs:
            api_params['params'] = kwargs.get('params', {})

        response = cls.api_client.call_api(method='GET', endpoint=cls.endpoint, **api_params)
        return [cls(**r) for r in response.json() if r]
    

    def create(self):
        '''
        Creates a new object in the API
        '''

        if 'create' not in self.actions:
            raise NotImplementedError(f'The "create" action is not implemented on {self.__class__.__name__}')

        request_body = {k: self.__dict__[k] for k in self.__dict__ if k in self.updatable_fields}
        if len(request_body) > 0:
            response = self.api_client.call_api(method='POST', endpoint=f'{self.endpoint}', json=request_body)
            return response
        return None


    def as_dict(self):
        return {k: self.__dict__.get(k, None) for k in self.__dict__ if k not in self.internal_fields}


    def __repr__(self):
        if hasattr(self, 'id'):
            return f"{self.__class__.__name__}(id={self.id})"
        else:
            return f"{self.__class__.__name__}("+", ".join([f"{k}={self.__dict__[k]}" for k in self.__dict__ if k not in self.internal_fields])+")"