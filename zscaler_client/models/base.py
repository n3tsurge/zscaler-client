import json
from json import JSONEncoder
from ..errors import *

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

    def __init__(self, client=None, *args, **kwargs):

        # The API client used to make API calls
        self.api_client = client
        self.updatable_fields = []
        self.actions = []
        self.approved_methods = []
        self.internal_fields = ['api_client', 'actions', 'updatable_fields']

        if (kwargs):
            for k in kwargs:
                self.__dict__[k] = kwargs.get(k, None)


    def update(self, **kwargs):
        '''
        Updates the model using the fields modified, used when updating a single field
        e.g. model.update(name="foo")
        '''

        if 'save' not in self.actions:
            raise ActionNotSupported(f'The "update" action is not supported on {self.__class__.__name__}')

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
            raise ActionNotSupported(f'The "save" action is not supported on {self.__class__.__name__}')

        request_body = {k: self.__dict__[k] for k in self.__dict__ if k in self.updatable_fields}
        if len(request_body) > 0:
            if hasattr(self, 'id'):
                self.api_client.call_api(method='PUT', endpoint=f'{self.endpoint}/{self.id}', json=request_body)
            else:
                self.api_client.call_api(method='POST', endpoint=f'{self.endpoint}', json=request_body)


    def as_dict(self):
        return {k: self.__dict__.get(k, None) for k in self.__dict__ if k not in self.internal_fields}


    def __repr__(self):
        if hasattr(self, 'id'):
            return f"{self.__class__.__name__}(id={self.id})"
        else:
            return f"{self.__class__.__name__}("+", ".join([f"{k}={self.__dict__[k]}" for k in self.__dict__ if k not in self.internal_fields])+")"