from fastapi import FastAPI,Path,HTTPException 
import json

app=FastAPI()

def load_data():
    with open('patient.json','r') as f:
        data=json.load(f)
    return data
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
        "resultoftest":data["P001"]["name"]
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






  
