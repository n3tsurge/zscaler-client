import json
from json import JSONEncoder
from ..errors import *
from ..client import get_client, APIClient


class CustomJsonEncoder2(json.JSONEncoder):
    def default(self, o):

        skip_fields = ['api_client', 'endpoint', 'internal_fields']
        if isinstance(o, JSONSerializable):
            return {k: o.__dict__[k] for k in o.__dict__ if k != skip_fields}

        if not isinstance(o, APIClient):
            return json.JSONEncoder.default(self, o)


class CustomJsonEncoder(json.JSONEncoder):
    def default(self, o):

        if isinstance(o, JSONSerializable):
            return o.__dict__

        if not isinstance(o, APIClient):
            return json.JSONEncoder.default(self, o)
        

class JSONSerializable(object):
    ''' Allows for an object to be represented in JSON format '''

    def jsonify(self):
        ''' Returns a json string of the object '''

        skip_fields = ['api_client', 'endpoint', 'internal_fields']
        for field in skip_fields:
            if field in self.__dict__:
                del self.__dict__[field]
        
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

    actions = []
    parameters = []
    required_fields = []
    required_parameters = []

    def __init__(self, client_alias='default', *args, **kwargs):

        # The API client used to make API calls
        self.api_client = get_client()
        self.internal_fields = ['api_client', 'actions', 'updatable_fields', 'internal_fields']

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
    def search(cls, endpoint=None, **kwargs):
        '''
        Performs search operations on a model
        '''

        if 'get' not in cls.actions:
            raise NotImplementedError(f'The "search" action is not implemented on {cls.__class__.__name__}')

        if not hasattr(cls, 'api_client'):
            cls.api_client = get_client()

        api_params = {}

        _endpoint = cls.endpoint

        if endpoint:
            _endpoint = endpoint

        api_params['params'] = {}

        if 'params' in kwargs:
            api_params['params'] = cls.parse_url_parameters(params=kwargs.get('params', {}))

        # Check to make sure any required parameters are supplied
        for p in cls.required_parameters:
            if p not in api_params['params']:
                raise MissingRequiredParameter(f'The "{p}" parameter is required.')

        response = cls.api_client.call_api(method='GET', endpoint=_endpoint, **api_params)

        # If this is a CSV download, just return the CSV content
        if response.headers['Content-Type'] == 'text/csv;charset=UTF-8':
            return response.text

        items = response.json()
        if isinstance(items, list):
            return [cls(**r) for r in items if r]
        else:
            return cls(**items)


    @classmethod
    def get(cls, id=None, **kwargs):

        if 'get' not in cls.actions:
            raise NotImplementedError(f'The "get" action is not implemented on {cls.__class__.__name__}')

        if not hasattr(cls, 'api_client'):
            cls.api_client = get_client()

        api_params = {}

        if 'params' in kwargs:
            api_params['params'] = cls.parse_url_parameters(kwargs.get('params', {}))

        # Check to make sure any required parameters are supplied
        for p in cls.required_parameters:
            if p not in api_params['params']:
                raise MissingRequiredParameter(f'The "{p}" parameter is required.')

        if id:
            return cls.search(endpoint=f"{cls.endpoint}/{id}", **api_params)
        else:
            return cls.search(endpoint=f"{cls.endpoint}", **api_params)


    @classmethod
    def parse_url_parameters(self, params):
        '''
        Parses URL parameters and only keeps the approved parameters for the model
        '''
        return {k: params[k] for k in params if k in self.parameters}

    
    @classmethod
    def get_client(cls):
        if not hasattr(cls, 'api_client'):
            cls.api_client = get_client()


    def create(self):
        '''
        Creates a new object in the API
        '''

        # If the model doesn't allow create throw a NotImplementedError
        if 'create' not in self.actions:
            raise NotImplementedError(f'The "create" action is not implemented on {self.__class__.__name__}')

        # Exclude fields that are not updatable
        request_body = {k: self.__dict__[k] for k in self.__dict__ if k in self.updatable_fields}

        # Check required fields
        for k in self.required_fields:
            if k not in request_body:
                raise MissingRequiredField(f'The field "{k}" is required.')

        # If there are fields in the request_body call the API
        if len(request_body) > 0:
            response = self.api_client.call_api(method='POST', endpoint=f'{self.endpoint}', json=request_body)
            if response.status_code == [400, 409]:
                raise RequestError(f'{response.status_code} - {response.message}')

            # Update the attributes of the item just created with the response from API
            if response._content != b'':
                self.__dict__.update(response.json())

        return None


    def delete(self):
        '''
        Deletes an object
        '''

        if 'delete' not in self.actions:
            raise NotImplementedError(f'The "delete" action is not implemented on {self.__class__.__name__}')

        response = self.api_client.call_api(method='DELETE', endpoint=f'{self.endpoint}/{self.id}')
        return responsible


    def as_dict(self):
        return {k: self.__dict__.get(k, None) for k in self.__dict__ if k not in self.internal_fields}


    def __repr__(self):
        if hasattr(self, 'id'):
            return f"{self.__class__.__name__}(id={self.id})"
        else:
            return f"{self.__class__.__name__}("+", ".join([f"{k}={self.__dict__[k]}" for k in self.__dict__ if k not in self.internal_fields])+")"