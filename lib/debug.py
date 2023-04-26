#!/usr/bin/env python3

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from faker import Faker
fake = Faker()

from models import Company, Dev, Freebie, session


if __name__ == '__main__':
    engine = create_engine('sqlite:///freebies.db')
    # Session = sessionmaker(bind=engine)
    # session = Session()
    # session.rollback()
  
    
    companies = session.query(Company).all()
    devs = session.query(Dev).all()
    freebies = session.query(Freebie).all()
    
    dev1=devs[0]
    company1 = companies[0]
    freebie1 = freebies[0]
    
    import ipdb; ipdb.set_trace()
