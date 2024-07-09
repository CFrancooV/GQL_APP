from sqlalchemy.orm import relationship,sessionmaker,declarative_base
from sqlalchemy import Column,String as dbString,Integer, ForeignKey

Base = declarative_base()

class Employer(Base):
    __tablename__ = "employers"
    id = Column(Integer, primary_key=True,autoincrement=True)
    name = Column(dbString)
    contact_email = Column(dbString)
    industry = Column(dbString)
    jobs = relationship("Job",back_populates="employer",lazy="joined") #establish relatanships to other tables linking the main clas Jon to back_populate the table employers

class Job(Base):
    __tablename__ = "jobs"
    id = Column(Integer,primary_key=True,autoincrement=True)
    title = Column(dbString)
    description = Column(dbString)
    employer_id = Column(Integer,ForeignKey("employers.id"))
    employer = relationship("Employer",back_populates="jobs",lazy="joined")
    applications = relationship("JobApplication",back_populates="job",lazy="joined")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True,autoincrement=True)
    user_name = Column(dbString)
    password_hash = Column(dbString)
    email = Column(dbString)
    role = Column(dbString)
    applications = relationship("JobApplication",back_populates="user",lazy="joined")

class JobApplication(Base):
    __tablename__ = "job_application"
    id = Column(Integer,primary_key=True,autoincrement=True)
    user_id = Column(Integer,ForeignKey("users.id"))
    job_id = Column(Integer,ForeignKey("jobs.id"))

    user = relationship("User",back_populates="applications",lazy="joined")
    job = relationship("Job",back_populates="applications",lazy="joined")