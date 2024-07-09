from graphene import String,Mutation,Field,Int
from graphql import GraphQLError
from app.DB.database import Session
from app.DB.models import User,JobApplication
from app.utils import generate_token,verify_password,get_auth_user,auth_user_same_as
from app.GQL.types import UserObjet,JobApplicationObject
from app.utils import hash_password,get_authenticated_user,admin_user

class  ApplyToJob(Mutation):
    class Arguments:
        user_id = Int(required = True)
        job_id  = Int(required = True)

    job_application = Field(lambda:JobApplicationObject)

    @auth_user_same_as
    def mutate(root,info,user_id,job_id):
        session = Session()
        existing_jobapplication = session.query(JobApplication).filter(
            JobApplication.user_id==user_id,
            JobApplication.job_id==job_id).first()

        if existing_jobapplication:
            raise GraphQLError("This user_id has applied to that job_id!")

        job_application = JobApplication(user_id=user_id,job_id=job_id)
        session.add(job_application)
        session.commit()
        session.refresh(job_application)
        session.close

        return ApplyToJob(job_application=job_application)

class LoginUser(Mutation):
    class Arguments:
        email = String(required = True)
        password = String(required = True)
    token = String()

    @staticmethod
    def mutate(root,info,email,password):
        session = Session()
        user = session.query(User).filter(User.email == email).first()

        if not user:
            raise GraphQLError("Not Registered Email please try Again")
        
        verify_password(user.password_hash,password)
        token = generate_token(email)
        return LoginUser(token=token)
    
class AddUser(Mutation):
    class Arguments:
        email = String(required=True)
        password = String(required = True)
        user_name = String(required=True)
        role = String(required=True)

    user = Field(lambda:UserObjet)
    
    @admin_user
    @staticmethod
    def mutate(root,info,email,password,user_name,role):

        if role == "Accountadmin":
            current_user = get_authenticated_user(info.context)
            if current_user.role != "Accountadmin":
                raise GraphQLError("You must be logged as Accountadmin, or you don't have Accountadmin role")


        session =Session()
        user = session.query(User).filter(User.email ==email).first()

        if user:
            raise GraphQLError("Email already in use, please try another")
        
        password_hash =  hash_password(password)
        user = User(user_name=user_name,email=email,password_hash=password_hash,role=role)
        session.add(user)
        session.commit()
        session.refresh(user)
        session.close()

        return AddUser(user=user)