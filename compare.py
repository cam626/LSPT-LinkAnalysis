#import relevant objects
import json

#Sort json object so that they can be compared
def ordered(obj):
    if isinstance(obj, dict):
        return sorted((k, ordered(v)) for k, v in obj.items())
    if isinstance(obj, list):
        return sorted(ordered(x) for x in obj)
    else:
        return obj

# Call as follows: print(ordered(jsona) == ordered(jsonb)) 
# would return: true or false
