#exporting pydantic models objs as python dict or json

from pydantic import BaseModel

class Address(BaseModel):
    city:str
    state:str
    pin:str

class Patient(BaseModel):
    name:str
    gender:str
    age:int
    address:Address

address_dict={'city':'Kolkata','state':'WB','pin':'700145'}
address_obj=Address(**address_dict)

patient_dict={'name':'Niladri','gender':'male','age':22,'address':address_obj}
patient_obj=Patient(**patient_dict)

temp_dict=patient_obj.model_dump() #converts the pydantic model objs to py_dict
'''
patient_obj.model_dump(params):
params may have :-
#include=['age','name'] which would only export name and age
#include=['name',{'address':['state','pin']}] which would only export the name and the state and pin from address
#exclude=['age','name'] which wouldn't export age and name
#exclude_unset=True say we have a def value of age and dont define it while creating the obj so it won't be exported
'''
print(temp_dict)
print(type(temp_dict))

temp_json=patient_obj.model_dump_json() #just received as str but exported as proper json
print(temp_json)
print(type(temp_json))



