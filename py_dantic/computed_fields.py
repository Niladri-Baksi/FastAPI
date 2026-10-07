from pydantic import BaseModel, EmailStr, AnyUrl, Field, computed_field
from typing import List, Dict, Optional, Annotated

class Patient(BaseModel):
    name: str
    email: EmailStr
    age: int
    linkedin: AnyUrl 
    weight: float 
    height: float
    married: bool 
    allergies: List[str]
    contact_details: Dict[str,str] 

    @computed_field
    @property
    def bmi(self)->float:
        bmi=round(self.weight/(self.height**2),2)
        return bmi


def insert_patient_data(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient.email)
    print(patient.linkedin)
    print(patient.weight)
    print(patient.married)
    print(patient.allergies)
    print(patient.contact_details)
    print('bmi=',patient.bmi)
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
              'height':1.80,
              'married': 0, 
              'allergies': ['smoke','skin'], 
              'contact_details':{'github':'https://github.com/Niladri-Baksi', 'phone':'6291140379','emergency':'9836188822'}} 

patient1= Patient(**patient_info)
 
insert_patient_data(patient1)
update_patient_data(patient1)