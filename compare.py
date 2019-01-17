#import relevant objects
import json

def listCompare(lis1, lis2):
  errors = 0
  i = 0
  for item1, item2 in zip(lis1, lis2):
    if item1 != item2:
      print("ERROR at element {0}: {1} != {2}".format(i, item1, item2))
      errors += 1
    i += 1
  return errors


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
