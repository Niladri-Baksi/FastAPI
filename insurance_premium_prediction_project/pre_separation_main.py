from attrs import field
from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field, field_validator
from typing import Annotated, Optional, List,Dict,Literal
import pickle
import pandas as pd

with open("model/model.pkl", "rb") as f:
    model = pickle.load(f)


MODEL_VERSION = "1.0.0"  # Define the model version manually but generally extracted from MLflow.

app = FastAPI()

#pydantic model for input data
class UserInput(BaseModel):
    age: Annotated[int, Field(..., gt=0,lt=120, description="Age of the user")]
    weight: Annotated[float, Field(..., gt=0, description="Weight of the user in kgs")]
    height: Annotated[float, Field(..., gt=0, lt=2.5, description="Height of the user in mtrs")]
    income_lpa: Annotated[float, Field(..., gt=0,description="Income of the user in LPA")]
    smoker: Annotated[bool, Field(..., description="Whether the user is a smoker or not")]
    city: Annotated[str, Field(..., description="City of the user")]
    occupation: Annotated[Literal['student', 'retired', 'self_employed', 'business_owner','private_job', 'unemployed', 'government_job'], Field(..., description="Occupation of the user")]

    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight / (self.height ** 2), 2)

    @computed_field
    @property
    def city_tier(self) -> str:
        tier1_cities = ["Mumbai", "Delhi", "Bangalore", "Hyderabad", "Ahmedabad", "Chennai", "Kolkata", "Pune", "Jaipur", "Surat"]
        tier2_cities = ["Lucknow", "Kanpur", "Nagpur", "Indore", "Thane", "Bhopal", "Visakhapatnam", "Pimpri-Chinchwad", "Patna", "Vadodara"]

        if self.city in tier1_cities:
            return 'Tier 1'
        elif self.city in tier2_cities:
            return 'Tier 2'
        else:
            return 'Tier 3'

    @field_validator('city')
    @classmethod
    def normalize_city(cls, v: str) -> str:
        return v.strip().title()  # Normalize city name to title case and remove leading/trailing spaces

    @computed_field
    @property
    def lifestyle_risk(self) -> str:
        if self.smoker and self.bmi > 30:
            return 'High'
        elif self.smoker or self.bmi > 30:
            return 'Medium'
        else:
            return 'Low'

    @computed_field
    @property
    def age_group(self) -> str:
        if self.age < 18:
            return 'Child'
        elif 18 <= self.age < 30:
            return 'Young Adult'
        elif 30 <= self.age < 50:
            return 'Adult'
        else:
            return 'Senior'


#human readable endpoint for the API
@app.get("/") 
def home():
    return {"message": "Welcome to the Insurance Premium Prediction API. Use the /predict endpoint to get predictions."}


#machine readable endpoint for the API like kubernetes, elastic load balancer, etc. can use this endpoint to check the health of the API...this will be forced to be done in order to deploy our api to the cloud servers like AWS, GCP, Azure, etc. since they will check the health of the API before routing the traffic to it.
@app.get("/health") 
def health_check():
    return {
        "status": "healthy",
        "version": MODEL_VERSION,
        "model_loaded": model is not None #not loaded will be false, loaded will be True
    }



@app.post("/predict")
def predict_premium(data: UserInput):
    # Convert the user data to a DataFrame
    input_df = pd.DataFrame([{
        'bmi': data.bmi,
        'age_group': data.age_group,
        'city_tier': data.city_tier,
        'lifestyle_risk': data.lifestyle_risk,
        'occupation': data.occupation,
        'income_lpa': data.income_lpa
    }])

    prediction = model.predict(input_df)[0] #output in list, since model.predict() is designed for multiple rows or batch predictions so getting the 1st element is viable here since we are only predicting for a single row of data. But for single row [0] is optional.
    return JSONResponse(status_code=200, content={"predicted_premium_category": prediction})
