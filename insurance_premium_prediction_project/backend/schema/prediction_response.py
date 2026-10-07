from pydantic import BaseModel, Field
from typing import Dict


#response model for validating the response or o/p of the prediction endpoint
class PredictionResponse(BaseModel):
    predicted_category: str = Field(..., description="The predicted insurance premium category", example="Medium")
    confidence: float = Field(..., description="The confidence score of the prediction", example=0.85)
    class_probabilities: Dict[str, float] = Field(..., description="The probabilities for each class label", example={"Low": 0.1, "Medium": 0.85, "High": 0.05})