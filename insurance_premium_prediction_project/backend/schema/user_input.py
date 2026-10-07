from pydantic import BaseModel, Field, computed_field, field_validator
from typing import Annotated, Optional, List,Dict,Literal
from config.city_tier import tier1_cities, tier2_cities

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