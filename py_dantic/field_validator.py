from pydantic import BaseModel, EmailStr, AnyUrl, Field, field_validator
from typing import List, Dict, Optional, Annotated


#field validator works only on one field and does 2 things...1. custom/personal data validation on fields like checking if a particular domain is in the email and 2. for transformations like if we want our patient name to be in caps

class Patient(BaseModel):
    name: str
    email: EmailStr
    age: int
    linkedin: AnyUrl 
    weight: float 
    married: bool 
    allergies: List[str]
    contact_details: Dict[str,str] 

    #field validator for custom datatypes for specific business usecases
    @field_validator('email') #decorator
    @classmethod 
    def email_validator(cls,value):
        valid_domains=['hdfc.com','icici.com'] #ex: abc@gmail.com
        domain_name=value.split('@')[-1]
        if domain_name not in valid_domains:
            raise ValueError('Not a valid domain')
        return value

    #field validator for transforations
    @field_validator('name')
    @classmethod
    def transform_name(cls,value):
        return value.upper()

    #field validator modes: before(value received before type coercion) and after(value received after type coercion)
    @field_validator('age',mode='after')
    @classmethod
    def validate_age(cls,value):
        if 0<value<100:
            return value
        else:
            raise ValueError('age should be in between 0 and 100')
    #so lets say we send the patient age as str '22'. if mode=before then value sent before type coercing from str to int hence it'll throw an error since str!=int else if mode=after then it'll type coerce str=>int and hence no error...default mode is after


def insert_patient_data(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient.email)
    print(patient.linkedin)
    print(patient.weight)
    print(patient.married)
    print(patient.allergies)
    print(patient.contact_details)
    print('inserted')

def update_patient_data(patient: Patient):
    print(patient.name)
    print(patient.age)
    print('updated')

patient_info={'name':'Niladri',
              'email':'niladri.baksi@icici.com',
              'linkedin':'https://www.linkedin.com/in/niladri-baksi/',
              'age':'22', 
              'weight':90.5, 
              'married': 0, 
              'allergies': ['smoke','skin'], 
              'contact_details':{'github':'https://github.com/Niladri-Baksi', 'phone':'6291140379'}} 

patient1= Patient(**patient_info)
 
insert_patient_data(patient1)
update_patient_data(patient1)