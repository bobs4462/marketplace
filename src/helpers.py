import json
from copy import deepcopy

# Below is a good example of how you should never write code

# Helper class for serialization of table records
class Serializable: 
    def json_serialize(self) -> str:
        fields = deepcopy(self.__dict__)
        del fields['_sa_instance_state']
        return json.dumps(fields)
