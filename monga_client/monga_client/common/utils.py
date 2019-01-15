import json
import time

def json_dump( _obj ):
    return json.dumps(_obj, 
                      sort_keys = True, 
                      indent = 4, 
                      ensure_ascii=False)
                      
def current_timestamp():
    return int(round(time.time()*1000))

class AttributeDict(dict): 
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
