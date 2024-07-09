
from graphene import List,String,ObjectType,Int,Field


class EmployeObject(ObjectType):
    id = Int()
    name = String()
    contact_email = String()
    industry = String()
    jobs = List(lambda: JobObject)  #only return value when needed so we avoid circular references

    @staticmethod
    def resolve_jobs(root,info):
        return root.jobs
        # return [job for job in jobs_data if job["employer_id"]== root["id"]]

class JobObject(ObjectType):
    id = Int()
    title = String()
    description = String()
    employer_id = Int()
    employer = Field(lambda: EmployeObject) 
    applications = List(lambda: JobApplicationObject)

    @staticmethod
    def resolve_employer(root,info):
        return root.employer
    @staticmethod
    def resolve_applications(root,info):
        return root.applications

class UserObjet(ObjectType):
    id = Int()
    user_name = String()
    email = String()
    role = String()
    applications = List(lambda: JobApplicationObject)

    @staticmethod
    def resolve_user_name(root,info):
        return root.user_name
    
    @staticmethod
    def resolve_applications(root,info):
        return root.applications
    
class JobApplicationObject(ObjectType):
    id = Int()
    user_id = Int()
    job_id = Int()
    user = Field(lambda:UserObjet)
    job = Field(lambda:JobObject)

    @staticmethod
    def resolve_user(root,info):
        return root.user
    
    @staticmethod
    def resolve_job(root,info):
        return root.job