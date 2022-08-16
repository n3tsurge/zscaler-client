
from .base import BaseModel

class RuleLabel(BaseModel):

    endpoint = "/ruleLabels"
    updatable_fields = ['name','description']
    actions = ['save','update','create']