import re

def num_parser(data):
    data = space_parser(data)
    match = re.match(r'[\d\.]+',data) or  re.match(r'-[\d\.]+',data)   # matches for a number and returns a match object
    if(match):
        return(data[match.end():])

def string_parser(data):
    data = space_parser(data)
    match = re.match(r'".*?"',data)      # matches for anything within double quotes and returns a match object
    if(match):
        return(data[match.end():])

def space_parser(data):                 # matches for white spaces and returns a match object 
    match=re.match(r'[\s\n]+',data)         
    if(match):
        return(data[match.end():])
    else:
        return(data)

def colon_parser(data):                 # matches for colon and returns a match object
    data = space_parser(data)       
    if(data[0] == ':'):                 
        return(data[1:])

def comma_parser(data):                 # matches for comma and returns a match object
    data = space_parser(data)      
    if(data[0] == ','):                 
        return(data[1:])

def boolean_parser(data):               # matches for a boolean value and returns a match object
    data = space_parser(data)
    if(data.startswith('true')):        
        return(data[4:])
    elif(data.startswith('false')):
        return(data[5:])

def null_parser(data):                  # matches for a null value and returns a match object
    data = space_parser(data)
    if(data.startswith('null')):        
        return(data[4:])

def object_parser(data):                # matches for a object and returns a match object
    data = space_parser(data)
    if(data[0]!='{'):
        return None
    data=data[1:]
    while(data[0]!='}'):
        data = string_parser(data)
        if(not data):
            return None
        data = colon_parser(data) 
        if(not data):
            return None    
        data = string_parser(data) or boolean_parser(data) or num_parser(data) or object_parser(data) or array_parser(data)
        if(not data):
            return None
        temp=comma_parser(data)
        if(temp):
            data=space_parser(temp)
            if(data[0]=='}'):
                return None
        else:
            data=space_parser(data)
            if(data[0]!='}'):
                return None   
    return(data[1:])     

def array_parser(data):                 # matches for an array and returns a match object
    data = space_parser(data)
    if(data[0]!='['):
        return None
    data=data[1:]
    while(data[0]!=']'):
        data = string_parser(data) or boolean_parser(data) or num_parser(data) or object_parser(data) or array_parser(data)
        if(not data):
            return None
        temp=comma_parser(data)
        if(temp):
            data=space_parser(temp)
            if(data[0]==']'):
                return None
        else:
            data=space_parser(data)
            if(data[0]!=']'):
                return None
    return(data[1:])

data='{"2":1}'
data=data+' '
A = object_parser(data) or array_parser(data) or boolean_parser(data) or string_parser(data) or num_parser(data) or null_parser(data)
if(not A):
    print('Invalid JSON')
else:
    A=A.strip()
    if(not A):
        print('Valid JSON')
    else:
        print('Invalid JSON')