from .base import BaseModel

class DataCenterVips(BaseModel):

    endpoint = '/vips/groupByDatacenter'
    parameters = [
        'routableIP', 'withinCountryOnly', 'includePrivateServiceEdge', 'includeCurrentVips',
        'sourceIp','latitude','longitude','subcloud'
    ]
    required_parameters = ['sourceIp']
    actions = ['get']

class PublicNode(BaseModel):

    endpoint = '/vips'
    parameters = ['dc', 'region','page','pageSize','include','subcloud']
    actions = ['get']

class GreTunnel(BaseModel):

    endpoint = '/greTunnels'
    actions = ['get','update','save','delete']
    parameters = ['page','pageSize']

class GreTunnelIPRange(BaseModel):

    endpoint = '/greTunnels/availableInternalIpRanges'
    paramers = ['internalIpRange', 'staticIp', 'limit']
    actions = ['get']

class OrgProvisioningGreTunnelInfo(BaseModel):

    endpoint = '/orgProvisioning/ipGreTunnelInfo'
    parameters = ['ipAddresses']
    actions = ['get']

class StaticIp(BaseModel):

    endpoint = '/staticIP'
    parameters = ['availableForGreTunnel','ipAddress','page','pageSize']
    updatable_fields = ['ipAddress', 'geoOverride', 'latitude', 'longitude', 'routableIP', 'comment']
    required_fields = ['latitude','longitude']
    actions = ['get','create','delete','update']