from fastapi import FastAPI,Path,HTTPException,Query
import json
from pydantic import BaseModel,Field,field_validator,model_validator,computed_field
from typing import Annotated,Literal
from fastapi.responses import JSONResponse
app=FastAPI()

class Patient(BaseModel):
    id:Annotated[str,Field(...,description='id of the patient',examples=['P001'])]
    name:Annotated[str,Field(...,description='name of the pateint')]
    city:Annotated[str,Field(...,description='city where the patient is living')]
    age:Annotated[int,Field(...,gt=0,le=100,description='age of the patient')]
    gender:Annotated[Literal['male','female','others'],Field(...,description='gender of the patient')]
    height:Annotated[float,Field(...,gt=0,description='height of the patient in meters')]
    weight:Annotated[float,Field(...,gt=0,description='weight of the patient in kgs')]

    @computed_field
    @property
    def bmi(self)->float:
        bmi=round(self.weight/(self.height**2),2)
        return bmi

    @computed_field
    @property
    def verdict(self)->str:
        if self.bmi < 18.5:
            return 'underweight'
        elif self.bmi <25:
            return 'normal'
        elif self.bmi < 30:
            return 'normal'
        else:
            return 'obese'

def load_data():
    with open('patient.json','r') as f:
        data=json.load(f)
    return data

def save_data(data):
    with open('patient.json','w') as f:
        json.dump(data,f)
    
@app.get("/")
def hello():
    return {
        "message":"patient management system api"
    }


@app.get("/about")
def about():
    return {
        "message":"a fully functional api to manage your patient records"
    }


@app.get("/view")
def view():
    data=load_data()

    return {
        #this is string literal
        #hardcoding 
        # "resultoftest":data["P001"]["name"]
         "resultoftest":data
    }

@app.get('/patient/{patient_id}')
def view_patient(patient_id:str=Path(...,description='ID of the patient in the DB',example='P001',min_length=4)):
    #load all the patients
    
    data=load_data()

    if patient_id in data:

        # return data[patient_id]
        # here patient id is variable literal 
        #so fastapi automatically gives patient_id="P001" so no quotation needed while accesing data
        return data[patient_id]
    raise HTTPException(status_code=404,detail='patient not found')



@app.get('/sort')
def sort_patients(sort_by:str=Query(...,description='sort on the basis of height weight or BMI',example='height'),order:str=Query('asc',description='sort in ascending or descending order')):
    valid_fields=['height','weight','BMI']
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400,detail=f'invalid field select from {valid_fields}')
    if order not in ['asc','desc']:
        raise HTTPException(status_code=400,detail='invalid order select between asc and desc')
    data=load_data()
    sort_order=True if order=='desc' else False
    sorted_data=sorted(data.values(),key=lambda x:x.get(sort_by,0),reverse=sort_order)
    return sorted_data
    
#post request 

@app.post('/create')
def create_patient(patient:Patient):
    #load existing data
    data=load_data()

    #check if the patient already exist 
    if patient.id in data:
        raise HTTPException(status_code=400,detail='patient already exist')
 
        
    #else new patient add to the database 
    data[patient.id]=patient.model_dump(exclude=['id'])
    #save into the json file

    save_data(data)
    return JSONResponse(status_code=201,content={
        'message':'patient created successfully'
    })

    










  
