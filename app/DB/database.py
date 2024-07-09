from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.DB.models import User,Base,Employer,Job,JobApplication
from app.DB.data import employers_data,jobs_data,user_data,applications_data
from app.Settings.config import DB_URL

print(DB_URL)

engine = create_engine(DB_URL) # Start the engine using the Database URL
Session = sessionmaker(bind=engine)


def prepare_database():
    from app.utils import hash_password
    
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    
    session = Session() #create te session just invoking the variable Session

    for employer in employers_data:
        # Employer(id=employer.get("id"), name = employer.get("name"), .... )
        emp = Employer(**employer)
        session.add(emp)

    for jobss in jobs_data:
        jo = Job(**jobss)
        session.add(jo)

    for user in user_data:
        user['password_hash'] = hash_password(user['password'])
        del user['password']
        session.add(User(**user))

    for application in applications_data:
        appl = JobApplication(**application)
        session.add(appl)

    session.commit()
    session.close()