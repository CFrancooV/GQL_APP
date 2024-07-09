from graphene import Field,String,Int,Mutation,Boolean
from app.DB.database import Session
from app.DB.models import Employer
from app.GQL.types import EmployeObject
from app.utils import SECRET_KEY,ALGORITHM,admin_user





        

class DeleteEmployer(Mutation):
    class Arguments:
        id = Int(required=True)

    success = Boolean()

    @admin_user
    @staticmethod
    def mutate(root,info,id):
        session = Session()
        employer = session.query(Employer).filter(Employer.id==id).first()

        if not employer:
            raise Exception("employer Id Not Found, PLease Try another ID")
        
        session.delete(employer)
        session.commit()
        session.close()
        return DeleteEmployer(success=True)

class UpdateEmployer(Mutation):
    class Arguments:
        id = Int(required=True)
        name = String()
        contact_email = String()
        industry = String()

    employer = Field(lambda:EmployeObject)

    @admin_user
    @staticmethod
    def mutate(root,info,id,name =None,contact_email=None,industry=None):
        session = Session()
        employer = session.query(Employer).filter(Employer.id == id).first()

        if not employer:
            raise Exception("Employer ID Not Found, Try with another ID")
        if name is not None:
            employer.name= name
        if contact_email is not None:
            employer.contact_email = contact_email
        if industry is not None:
            employer.industry = industry

        session.commit()
        session.refresh(employer)
        session.close()
        return UpdateEmployer(employer=employer)
    
class CreateEmployer(Mutation):
    class Arguments:
        name = String(required=True)
        contact_email= String(required=True)
        industry = String(required=True)

    employer = Field(lambda:EmployeObject)

    @admin_user
    @staticmethod
    def mutate(root,info,name,contact_email,industry):
        session = Session()
        employer = Employer(name=name,contact_email=contact_email, industry=industry)
        session.add(employer)
        session.commit()
        session.refresh(employer)
        session.close()
        return CreateEmployer(employer=employer)
        