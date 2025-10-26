from pydantic import BaseModel,EmailStr,AnyUrl,Field,field_validator,model_validator,computed_field
from typing import List,Dict,Optional,Annotated

class Patient(BaseModel):
    # name:str=Field(max_legth=20)
    name:Annotated[str,Field(max_length=2,title='name of the patient',description='give name less than 50 character',examples=['Nitish','sita'])]
    age:int=Field(gt=0,le=120)
    linkedin_url:AnyUrl
    email:str
    weight:Annotated[float,Field(gt=0,strict=True)]
    # weight:float=Field(gt=0)
    # married:bool=False
    married:Annotated[bool,Field(default=None,description='is the patient married ot not')]
    allergies:Optional[List[str]]=None
    contact_details:Dict[str,str]
    height:float

    @field_validator('email')
    @classmethod
    def email_validator(cls,value):
        valid_domains=['hdfc.com','iccici.com']
        domain_name=value.split('@')[-1]
        if domain_name not in valid_domains:
            raise ValueError('not a valid domain')
        return value

    @field_validator('name')
    @classmethod
    def transform_name(cls,value):
        return value.upper()

    @field_validator('age',mode='after')
    @classmethod
    def validate_age(cls,value):
        if 0<value<100:
            return value
        else:
            raise ValueError("age less or greater")

    @model_validator(mode='after')
    def validate_emergency_contact(cls,model):
        if model.age>60 and 'emergency' not in model.contact_details:
            raise ValueError('patients older than 60 muyst have an e,ergency contact number')
        return model
    
    @computed_field
    @property
    def calculate_bmi(self)->float:
        #calculate_bmi act as a field name 
        bmi=round(self.weight/(self.height**2),2)
        return bmi


def insert_patient_data(patient:Patient):
    print(patient.name)
    print(patient.age)
    print(patient.contact_details)
    print(patient.married)
    print(patient.allergies)
    print(patient.linkedin_url)
    #so here there is calculate_bmi
    print(patient.calculate_bmi)



patient_info={
    'name':'u',
    'age':'65',
    'email':'abchdfc.com',
    'weight':75.2,
    'height':1.72,
    'married':True,
    'linkedin_url':'https://www.linkedin.com/in/unika-tamang-1aa522290/',
    'allergies':['pollen','dust'],
    'contact_details':{
        'email':'abc@gmail.com',
        'phone':'1234',
        'emergency':'1234'
    }


}
patient1=Patient(**patient_info
)

insert_patient_data(patient1)



