from pydantic import BaseModel, EmailStr, AnyUrl, Field
from typing import List, Dict, Optional, Annotated

class Patient(BaseModel): #the class must import BaseModel class to be a pydantic class
    name: Annotated[str, Field(max_length=50,title='Name of the patient',description='in less than 50 char',examples=['Nitish','Niladri'])] #field fn is used for custom data validation, along with adding default values also its used for suppressing auto type coercion by pydantic. Annotated is used along with it for adding additional metadata
    age: Annotated[int, Field(default=None,gt=0,lt=120,description='enter the valid age of the patient')]
    email: EmailStr #custom datatype for email data validation
    linkedin: AnyUrl #custom datatype for url data validation
    weight: float = Field(gt=0,strict=True,default=30.5) #its used for suppressing auto type coercion by pydantic and for adding a def value
    married: bool = False #def value would be False
    allergies: Optional[List[str]] = None #its an optional field, with def value none
    contact_details: Dict[str,str] #used instead of just dict cuz we need 3 level of validations 1. contact_details must be dict and 2. the key and the 3. value must have only str

#field fn: custom data validation, suppressing auto type coercion, adding a def value and used within Annotated to add additional metadata

# def insert_patient_data(name,age):
#     print(name)
#     print(age)
#     print('inserted')

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
              'email':'niladri.baksi@gmail.com',
              'linkedin':'https://www.linkedin.com/in/niladri-baksi/',
              'age':22, #'22' gets implicitly converted to 22 int by pydantic but 'twenty-two' will be treated as a str
              'weight':90.5, 
              'married': 0, 
              'allergies': ['smoke','skin'], 
              'contact_details':{'github':'https://github.com/Niladri-Baksi', 'phone':'6291140379'}} 

patient1= Patient(**patient_info) #**dict unpacks a dictionary into keyword arguments like to Patient(name='Niladri', age=22)
#now on running the code the rules of the Patient class will be applied on patient_info, if it satisfies all rules we will have a patient1 obj to be used
 
insert_patient_data(patient1)
update_patient_data(patient1)