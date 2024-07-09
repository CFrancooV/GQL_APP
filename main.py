from graphene import Schema
from fastapi import FastAPI
from starlette_graphene3 import GraphQLApp,make_playground_handler

from app.DB.database import prepare_database, Session
from app.DB.models import Employer,Job
from app.GQL.queries import Query
from app.GQL.mutations import Mutation

schema = Schema(query = Query, mutation=Mutation)

app = FastAPI()


def startup_event():
    prepare_database()
app.add_event_handler("startup", startup_event)

@app.get("/employers")
def get_employers():
    with Session() as session:
        return session.query(Employer).all()

@app.get("/jobs")
def get_jobs():
    with Session() as session:
        return session.query(Job).all()

app.mount("/",GraphQLApp(
    schema=schema,
    on_get = make_playground_handler()
))


