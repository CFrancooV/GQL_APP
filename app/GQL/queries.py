from graphene import ObjectType,List,Field,Int
from app.GQL.types import JobObject,EmployeObject,UserObjet,JobApplicationObject

from app.DB.data import jobs_data,employers_data
from app.DB.database import Session
from app.DB.models import Job,Employer,User,JobApplication
from sqlalchemy.orm import joinedload

class Query(ObjectType):
    jobs = List(JobObject)
    job = Field(JobObject,id = Int(required = True))

    employers = List(EmployeObject)
    employer = Field(EmployeObject,id = Int(required = True))

    users = List(UserObjet)
    user = Field(UserObjet,id = Int(required = True))

    jobs_application = List(JobApplicationObject)
    job_application = Field(JobApplicationObject,id = Int(required = True))

    @staticmethod
    def resolve_job(root,info,id):
        return Session().query(Job).filter(Job.id == id).first()

    @staticmethod
    def resolve_jobs(root,info):
        return Session().query(Job).options(joinedload(Job.employer)).all()
        #return Session().query(Job).all()

    @staticmethod
    def resolve_employer(root,info,id):
        return Session().query(Employer).filter(Employer.id == id).first()

    @staticmethod
    def resolve_employers(root,info):
        return Session().query(Employer).options(joinedload(Employer.jobs)).all()
        return Session().query(Employer).all()
    
    @staticmethod
    def resolve_user(root,info,id):
        return Session().query(User).filter(User.id == id).first()

    @staticmethod
    def resolve_users(root,info):
        return Session().query(User).all()

    
    @staticmethod
    def resolve_job_application(root,info,id):
        return Session().query(JobApplication).filter(JobApplication.id == id).first()
    
    @staticmethod
    def resolve_jobs_application(root,info):
        return Session().query(JobApplication).all()