from attrs import field
from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Optional, List,Dict,Literal
import json

app=FastAPI()

#PYDANTIC MODEL
class Patient(BaseModel):
    id: Annotated[str, Field(..., description="ID of the patient",example="P001")]
    name: Annotated[str, Field(..., description="Name of the patient",example="Niladri Baksi")]
    city: Annotated[str, Field(..., description="City of the patient",example="Guwahati")]
    age: Annotated[int, Field(..., description="Age of the patient",example=22,gt=0,lt=120)] 
    gender: Annotated[Literal["male", "female","other"], Field(..., description="Gender of the patient",example="male")] #Literal[] in Python is a type-hinting tool used to restrict a variable, function argument, or return value to specific, exact values rather than just a general data type.
    height: Annotated[float, Field(..., description="Height of the patient in mtrs",example=1.85)]
    weight: Annotated[float, Field(..., description="Weight of the patient in kgs",example=90.5)]

    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight / (self.height ** 2), 2)

    @computed_field
    @property
    def verdict(self) -> str:
        bmi_value = self.bmi
        if bmi_value < 18.5:
            return "Underweight"
        elif 18.5 <= bmi_value < 25:
            return "Normal weight"
        elif 25 <= bmi_value < 30:
            return "Overweight"
        else:
            return "Obesity"


#building a new pydantic model with non-mandatory or optional fields for updating existing patient data
class PatientUpdate(BaseModel):
    #id is path parameter so we don't need to include it in the request body, hence not included in this model
    name: Annotated[Optional[str], Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None)]
    gender: Annotated[Optional[Literal["male", "female","other"]], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None)]
    weight: Annotated[Optional[float], Field(default=None)]


#HELPER FUNCTIONS
def load_data():
    with open('patients.json','r') as f:
        data=json.load(f)
    return data

def save_data(data):
    with open('patients.json','w') as f:
        json.dump(data,f,indent=4)


# RETRIEVE
@app.get("/")
def hello():
    return{'message':'Patient Management System API'}

@app.get('/about')
def about():
    return{'message':'A fully functional API to manage patient records'}

@app.get('/view') #getting all patients data
def view():
    data=load_data()
    return data

@app.get('/patient/{patient_id}') #patient_id is a path parameter
def view_patient(patient_id : str = Path(..., description='ID of the patient in DB', example='P001')): #since str in json, ...represents the params are required
    data=load_data()
    if patient_id in data:
        return data[patient_id] #since data has key:value so if patient id matches it returns all the corresponding values of it
    raise HTTPException(status_code=404, detail='Patient not found') #raises 404 not found code
    # return {'error':'patient not found'} #returns a 200 success code

@app.get('/sort')
def sort_patients(sort_by : str = Query(..., description='sort on the basis of height, weight or bmi'), order : str = Query('asc', description='sort in asc or desc order')): #sort_by is a required query param '...' and order is an optional query param where asc is the default value

    valid_fields=['height','weight','bmi']

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400,detail=f'invalid field...select from {valid_fields}')
    if order not in ['asc','desc']:
        raise HTTPException(status_code=400,detail='invalid order...select between asc and desc')  

    data=load_data()

    sort_order=True if order=='desc' else False

    sorted_data=sorted(data.values(), key=lambda x:x.get(sort_by, 0), reverse=sort_order) # lambda function takes each patient dictionary (x), retrieves the value of the field selected by the user (height, weight, or bmi) using x.get(sort_by, 0), and returns that value to sorted() as the sorting key. Thus, patients are sorted based on the selected field, while 0 acts as a fallback if the field is missing.

    return sorted_data


#CREATE
@app.post('/create') #adding a new patient
def add_patient(patient: Patient): #request body data goes to pydantic model for validation and then the validated data is passed to the function as a Patient object
    #load existing data from the JSON file
    data=load_data()

    #check if the patient ID already exists in the data
    if patient.id in data:
        raise HTTPException(status_code=400, detail='Patient already exists')

    #add the new patient data to the existing data
    data[patient.id]=patient.model_dump(exclude=['id']) #model_dump() method converts the pydantic model to a dictionary including the calculated bmi and verdict... key-value pairs, excluding the 'id' field since it's already used as the key in the data dictionary.

    #save into the json file
    save_data(data)

    return {JSONResponse(status_code=201, content={'message':'Patient added successfully'})} #returns a 201 created code

    '''
    req body data goes to pydantic model for validation and then the validated and calculated data is passed to the function as a Patient object

    data loaded in a dictionary from the json file, 
    
    if the patient ID already exists in the data, a 400 bad request response is returned. 
    
    Otherwise, the new patient data is added to the existing data dictionary with the patient ID as the key and the rest of the patient data as the value. 
    
    The model_dump() method is used to convert the pydantic model to a dictionary, excluding the 'id' field since it's already used as the key in the data dictionary. 
    
    Finally, the updated data is saved back to the json file and a 201 created response is returned.
    
    '''


#UPDATE
@app.put('/edit/{patient_id}')
def update_patient(patient_id: str, patient_update: PatientUpdate): #request body data goes to pydantic model for validation and then the validated data is passed to the function as a PatientUpdate object

    data=load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient not found')

    #update the existing patient data with the new data from the request body
    existing_patient=data[patient_id]
    existing_patient_cpy=existing_patient.copy() #create a copy of the existing patient data to avoid modifying it directly
    updated_patient=patient_update.model_dump(exclude_unset=True) #model_dump(exclude_unset=True) returns a dictionary of only the fields that were provided in the request body, excluding any fields that were not set (i.e., left as None). This allows us to update only the fields that were provided in the request body, while leaving the other fields unchanged.

    for key, value in updated_patient.items(): #model_dump(exclude_unset=True) returns a dictionary of only the fields that were provided in the request body, excluding any fields that were not set (i.e., left as None). This allows us to update only the fields that were provided in the request body, while leaving the other fields unchanged.
        existing_patient[key]=value


    #existing_patient_cpy->pydantic object of the Patient class->updated bmi+verdict
    existing_patient['id']=patient_id #add the patient id to the updated patient data dictionary, since it is not included in the request body and is needed to create a new Patient object
    patient_pydantic_obj=Patient(**existing_patient) #create a new Patient object with the updated data and the existing patient ID

    #pydantic_obj->dict
    existing_patient=patient_pydantic_obj.model_dump(exclude='id') #convert the updated Patient object back to a dictionary, including the calculated bmi and verdict

    data[patient_id]=existing_patient

    save_data(data)

    return {JSONResponse(status_code=200, content={'message':'Patient updated successfully'})}

'''
So first we get the patient id as the path param and the func takes in that patient id and the request body data goes to pydantic model(where the fields are non mandatory so only some fields can be passes not necessarily all) for validation and then the validated data is passed to the function as a PatientUpdate object

Then the data is loaded and the value corresponding to the patient id provided is stored in existing_patient variable and a copy of it is created to avoid modifying it directly.
Then in updated_patient variable we store the dictionary of only the fields that were provided in the request body, excluding any fields that were not set (i.e., left as None). This allows us to update only the fields that were provided in the request body, while leaving the other fields unchanged.

Then we loop through the updated_patient dictionary and update the existing_patient dictionary with the new values. So key of the updated_patient dictionary is used to access the corresponding value in the existing_patient dictionary and update it with the new value.

But the problem arises when the user updates the height or weight of the patient, then the bmi and verdict will not be updated since they are calculated fields and are not included in the request body or in the PatientUpdate model. 
So to solve this we create a new Patient object patient_pydantic_obj with the updated data and the existing patient ID and then convert it back to a dictionary, including the calculated bmi and verdict. Since in the Patient model all the fields are mandatory so id must be included in it and since we defined bmi and verdict as computed fields, so when we create a new Patient object with the updated data, the bmi and verdict will be automatically recalculated based on the new height and weight values.

Then we convert the updated Patient object back to a dictionary, including the calculated bmi and verdict excluding the existing patient ID 
and then we update the data dictionary with the updated patient data corresponding to the patient ID and save it back to the json file and return a 200 success code.

'''


#DELETE
@app.delete('/delete/{patient_id}')
def delete_patient(patient_id: str):
    data=load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient not found')

    del data[patient_id]

    save_data(data)

    return {JSONResponse(status_code=200, content={'message':'Patient deleted successfully'})}