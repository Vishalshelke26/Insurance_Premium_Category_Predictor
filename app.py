from turtle import pd
import pandas as pd 
from fastapi.responses import JSONResponse
from fastapi import FastAPI
from pydantic import BaseModel, Field, computed_field
from typing import Literal , Annotated
import pickle


tier_1_cities = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Pune"]
tier_2_cities = [
    "Jaipur", "Chandigarh", "Indore", "Lucknow", "Patna", "Ranchi", "Visakhapatnam", "Coimbatore",
    "Bhopal", "Nagpur", "Vadodara", "Surat", "Rajkot", "Jodhpur", "Raipur", "Amritsar", "Varanasi",
    "Agra", "Dehradun", "Mysore", "Jabalpur", "Guwahati", "Thiruvananthapuram", "Ludhiana", "Nashik",
    "Allahabad", "Udaipur", "Aurangabad", "Hubli", "Belgaum", "Salem", "Vijayawada", "Tiruchirappalli",
    "Bhavnagar", "Gwalior", "Dhanbad", "Bareilly", "Aligarh", "Gaya", "Kozhikode", "Warangal",
    "Kolhapur", "Bilaspur", "Jalandhar", "Noida", "Guntur", "Asansol", "Siliguri"
]


#import models

with open("C:/Users/vishal/OneDrive/Desktop/fast_api/model.pkl", "rb") as f:
    model = pickle.load(f)

app = FastAPI()

#pydantic model to validate the request body
class UserInput(BaseModel):
    age : Annotated[int,Field(...,gt=0,lt=100,title="age of the user",description="give the age of the user in years",examples=[27])]
    weight : Annotated[float,Field(...,gt=0,title="weight of the user",description="give the weight of the user in kgs",examples=[70.00])]
    height : Annotated [float,Field(gt=0,title="height of the user",description="give the height of the user in cms",examples=[170.00])]
    income_lpa:Annotated[float,Field(...,gt=0,title="income of the user",description="give the income of the user in lpa",examples=[5.00])]
    smoker: Annotated[bool,Field(...,title="smoker",description="indicates if the user is a smoker",examples=[False])]
    city: Annotated[str,Field(...,title="city",description="the city where the user lives",examples=["Gurgaon"])]
    occupation: Annotated[str,Field(...,title="occupation",description="the occupation of the user",examples=["government_job"])]


    @computed_field
    @property
    def BMI(self) -> float:
        return self.weight / ((self.height/100)**2)


    @computed_field
    @property
    def lifestyle_risk(self) -> str:
        if (self.smoker and self.BMI > 30 and self.age_group in ["senior", "middle_aged"]):
            return "high"

        elif (self.smoker or (self.BMI > 27 and self.age_group in ["middle_aged", "adult"])):
            return "medium"

        else:
            return "low"

    @computed_field
    @property
    def age_group(self) -> str:
        if self.age < 25:
            return "young"
        elif self.age < 45:
            return "adult"
        elif self.age < 60:
            return "middle_aged"
        return "senior"

    @computed_field
    @property
    def city_tier(self) -> int:
        if self.city in tier_1_cities:
            return 1
        elif self.city in tier_2_cities:
            return 2
        else:
            return 3

        

@app.post('/predict')
def predict_premium(data: UserInput):

    input_df = pd.DataFrame([{
        'BMI': data.BMI,
        'age_group': data.age_group,
        'lifestyle_risk': data.lifestyle_risk,
        'city_tier': data.city_tier,
        'income_lpa': data.income_lpa,
        'occupation': data.occupation
    }])

    prediction = model.predict(input_df)[0]

    return JSONResponse(status_code=200, content={'predicted_category': prediction})



