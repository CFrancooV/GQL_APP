from graphene import Field,String,Int,Mutation,Boolean
from app.DB.database import Session
from app.DB.models import Job
from app.GQL.types import JobObject
from app.utils import admin_user

class AddJob(Mutation):  #Initialize the mutation by adding a job
    class Arguments: # initialize the class of the arguments of the mutation title, description and employer_id id will be added incelemtally and managed by SQLAlmchemy sequence generators automatically due to the specs on models
        title = String(required=True)  
        description = String(required=True)
        employer_id = Int(required = True)

    job = Field(lambda:JobObject)  #set the job to be a field and evaluate only when needed from the imported JobObject

    @admin_user #change to static method so we can reference the root and avoid missviheavours with self
    @staticmethod
    def mutate(root,info,title,description,employer_id): #mutate is the defined keyword for mutations and pass their arguments
        job = Job(title = title, description = description,employer_id=employer_id) #initalize the job and each argument so it can be recogniced by the imported Job
        session = Session()   #Call the ssesion to interact qith the database
        session.add(job) #add the job to the session, this method will add automatically the job to our database but is in pending state till commited
        session.commit() #Commint to succesfully add the job
        session.refresh(job) ## Refresh the job object to reflect any database-triggered updates
        session.close()  # Close the session to release resources
        return AddJob(job=job) # Return the AddJob instance with the newly added job object, This ensures the mutation returns the newly added job data

class UpdateJob(Mutation): #Uodate bases on Id input and optional arguments
    class Arguments:
        id = Int(required=True)
        title = String()
        description = String()
        employer_id = Int()

    job = Field(lambda:JobObject)

    @admin_user
    @staticmethod
    def mutate(root,info,id,title=None,description=None, emplopyer_id=None):
        session = Session()
        job = session.query(Job).filter(Job.id == id).first()
        #job = session.query(Job).options(joinedload(Job.employer)).filter(Job.id == id).first()

        if not job:
            raise Exception("Job ID not found")
        if title is not None:
            job.title = title
        if description is not None :
            job.description = description
        if emplopyer_id is not None:
            job.employer_id = emplopyer_id

        session.commit()
        session.refresh(job) 
        session.close()
        return UpdateJob(job = job)

class DelteJob(Mutation):
    class Arguments:
        id = Int(required=True)

    success = Boolean()

    @admin_user
    @staticmethod
    def mutate(root,info,id):
        session = Session()
        job = session.query(Job).filter(Job.id==id).first()

        if not job:
            raise Exception("ID Job Not Found")
        
        session.delete(job)
        session.commit()
        session.close()
        return DelteJob(success=True)