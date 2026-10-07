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

print(patient_obj)
print(patient_obj.address.pin)

'''
Nested Models:
# Better organization of related data like address, vitals, insurance
# Reusability like using address in multiple models
# Readability like easier for devs and API consumers to understand
# Validation like nested models are validated automatically, no extra work needed
'''
