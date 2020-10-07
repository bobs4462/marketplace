import json
from enum import Enum
from copy import deepcopy

# Below is a good example of how you should never write code

# Helper class for serialization of table records
class Serializable: 
    def json_serialize(self) -> str:
        fields = deepcopy(self.__dict__)
        del fields['_sa_instance_state']
        return json.dumps(fields)

class ValidationStatus(Enum):
    OK = 'correct value'
    IS_EMPTY = 'is not provided'
    IS_NOT_INT = 'is not a valid integer'

def validate_int(value) -> ValidationStatus:
    # None check
    if not value:
        return ValidationStatus.IS_EMPTY
    # let's check that requested value is a valid integer
    if type(value) is not int:
        return ValidationStatus.IS_NOT_INT
    return ValidationStatus.OK


