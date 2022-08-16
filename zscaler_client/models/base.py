import json
from json import JSONEncoder

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

    def __init__(self, client, *args, **kwargs):

        # The API client used to make API calls
        self.api_client = client

        if (kwargs):
            for k in kwargs:
                self.__dict__[k] = kwargs.get(k, None)


    def update(self, **kwargs):
        '''
        Updates the model using the fields modified, used when updating a single field
        e.g. model.update(name="foo")
        '''

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

        request_body = {k: self.__dict__[k] for k in self.__dict__ if k in self.updatable_fields}
        if len(request_body) > 0:
            self.api_client.call_api(method='PUT', endpoint=f'{self.endpoint}/{self.id}', json=request_body)


    def as_dict(self):
        return {k: self.__dict__.get(k, None) for k in self.__dict__ if k not in ['api_client']}


    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id})"