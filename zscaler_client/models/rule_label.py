class RuleLabel(object):

    def __init__(self, client, *args, **kwargs):

        self.client = client

        if (kwargs):
            for k in kwargs:
                self.__dict__[k] = kwargs.get(k, None)


    def update(self, name=None, description=None):

        request_body = {}
        if name:
            request_body['name'] = name

        if description:
            request_body['description'] = description

        if request_body == {}:
            request_body = {
                'name': self.name,
                'description': self.description
            }

        self.client.call_api(method='PUT', endpoint=f'/api/v1/ruleLabels/{self.id}', json=request_body)

    def __repr__(self):
        return f"RuleLabel(id={self.id}, name={self.name})"