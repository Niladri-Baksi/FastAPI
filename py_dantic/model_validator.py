from pydantic import BaseModel, EmailStr, AnyUrl, Field, model_validator
from typing import List, Dict, Optional, Annotated

#model_validator can be used for data validation by combining more than one fields like for fields depending on other fields
class Patient(BaseModel):
    name: str
    email: EmailStr
    age: int
    linkedin: AnyUrl 
    weight: float 
    married: bool 
    allergies: List[str]
    contact_details: Dict[str,str] 

    #model_validator for checking if age>60 then contact_details must have one emergency contact else patient won't be admitted
    @model_validator(mode='after')
    def validate_emergency_contact(cls, model):
        if model.age > 60 and 'emergency' not in model.contact_details:
            raise ValueError('Patients older than 60 mist have an emergency contact')
        return model


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
              'age':'82', 
              'weight':90.5, 
              'married': 0, 
              'allergies': ['smoke','skin'], 
              'contact_details':{'github':'https://github.com/Niladri-Baksi', 'phone':'6291140379','emergency':'9836188822'}} 

patient1= Patient(**patient_info)
 
insert_patient_data(patient1)
update_patient_data(patient1)