
from .base import BaseModel

class RuleLabel(BaseModel):

    endpoint = "/ruleLabels"
    updatable_fields = ['name','description']
    approved_methods = ['GET','POST','PUT']
    actions = ['save','update']