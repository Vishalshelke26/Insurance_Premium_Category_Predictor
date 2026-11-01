from pydantic import BaseModel , EmailStr , AnyUrl , Field
from typing import List , Dict , Optional , Annotated

class  Patient(BaseModel):

    name : Annotated[str,Field(max_length=50,title="name of the patient",description="give the name of the patient in less than 50 chars",examples=["vishal"])]
    age : int 
    weight : float = Field(gt = 0)
    married : Annotated[bool,Field(default=None, description="Is the patient married or not")]
    allergies : Optional[List[str]] = None
    contact_details : Dict[str,str]


patient_info = {"name" : "vishal","age": 27,"weight": 70.00, "married":False,"allergies":["pollen dust"],"contact_details":{"email":"vishal.shelke0369@gmail.com","phone": "987654321"}}

patient1 = Patient(**patient_info)

def insert_patient_data(patient1 : Patient):
    print(patient1.name)
    print(patient1.age)
    print(patient1.allergies)
    print("inserted")


insert_patient_data(patient1)