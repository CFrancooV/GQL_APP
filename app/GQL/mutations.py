
from graphene import ObjectType
from app.GQL.Job.mutations import AddJob,UpdateJob,DelteJob
from app.GQL.Employer.mutations import CreateEmployer,UpdateEmployer,DeleteEmployer
from app.GQL.User.mutations import LoginUser,AddUser,ApplyToJob
    
class Mutation(ObjectType): # Define the Mutation class to expose mutation fields
    add_job = AddJob.Field()  # Expose the AddJob mutation as a field in the GraphQL schema
    update_job = UpdateJob.Field()
    delete_job = DelteJob.Field()
    create_employer = CreateEmployer.Field()
    update_employer = UpdateEmployer.Field()
    delete_employer = DeleteEmployer.Field()
    login_user = LoginUser.Field()
    add_user = AddUser.Field()
    apply_to_job = ApplyToJob.Field()