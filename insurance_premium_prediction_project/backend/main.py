from attrs import field
from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from schema.user_input import UserInput
from model.predict import predict_output, MODEL_VERSION, model
from schema.prediction_response import PredictionResponse

#model loading and version was here now moved to model/predict.py

app = FastAPI()


#pydantic model was here in this file but moved to schema/user_input.py to keep the code clean and organized.

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


@app.post("/predict", response_model=PredictionResponse)
def predict_premium(data: UserInput):
    # Convert the user data to a Dict
    user_input = {
        'bmi': data.bmi,
        'age_group': data.age_group,
        'city_tier': data.city_tier,
        'lifestyle_risk': data.lifestyle_risk,
        'occupation': data.occupation,
        'income_lpa': data.income_lpa
    }

    try:
        prediction = predict_output(user_input)  #Call the predict_output function from model/predict.py
        return JSONResponse(status_code=200, content={"predicted_premium_category": prediction})
    except Exception as e:
        raise JSONResponse(status_code=500, content={"error": str(e)})
