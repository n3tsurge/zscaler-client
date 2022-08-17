from .base import BaseModel

class AdminRoleLite(BaseModel):

    endpoint = '/adminRoles/lite'
    parameters = ['includeAuditorRole', 'includePartnerRole']
    actions = ['get']


class AdminUser(BaseModel):

    endpoint = '/adminUsers'
    parameters = ['includeAuditorUsers', 'includeAdminUsers', 'search', 'page', 'pageSize']
    updatable_fields = [
        'loginName','userName','email','role','comments','adminScope','isNonEditable',
        'disabled','isAuditor','password','isPasswordLoginAllowed', 'isSecurityReportCommEnabled',
        'isServiceUpdateCommEnabled', 'isProductUpdateCommEnabled', 'isPasswordExpired',
        'isExecMobileAppEnabled', ''
    ]
    required_fields = ['userName', 'loginName', 'email']