from pydantic import BaseModel
class Address(BaseModel):
    city:str
    state:str
    pin:str


class Patient(BaseModel):
    name:str
    gender:str
    age:int
    '''
    since here address hold multiple value simple
     it is complex datatype so we create diff model for address
    '''
    # address:'kapan 12 budhanilkantha'
    #so here the use of nested model comes in
    address:Address


address_dict={
    'city':'gur',
    'state':'hariyana',
    'pin':'1234'
}

adress1=Address(**address_dict)
patient_dict={
    'name':'nimesh',
    'gender':'male',
    'age':20,
    'address':adress1
}
def details(patient:Patient):
    print(patient.name)
    print(patient.age)
    print(patient.gender)
    print(patient.address)

patient1=Patient(**patient_dict)
# print(patient1.address.pin)
# # details(patient1)

#model_dump gives the dictionary of pydantic model object
#we can use include attribute to show the respecive fields
# temp=patient1.model_dump(include=['name'])
#for state insdie adress then

temp=patient1.model_dump(exclude={
    'address':['state']
})
print(temp)
#it gives dict
print(type(temp))
'''
for json we 
will use model_dump_json()
'''

# t=patient1.model_dump_json()
# print(t)
# print(type(t))

