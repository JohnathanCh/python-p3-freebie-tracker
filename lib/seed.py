#!/usr/bin/env python3

from random import choice as rc
from faker import Faker
fake = Faker()

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Company, Dev, Freebie

engine = create_engine('sqlite:///freebies.db')
Session = sessionmaker(bind=engine)
session = Session()

print("deleting records")
def delete_records():
    session.query(Company).delete()
    session.query(Dev).delete()
    session.query(Freebie).delete()
    session.commit()

print("creating new records")
def create_records():
    companies = [Company(name=fake.company(), founding_year=int(fake.year())) for i in range(50)]
    devs = [Dev(name=fake.name()) for i in range(1000)]
    freebies = [Freebie(item_name=fake.word(), value=rc(range(2000))) for i in range(5000)]
    session.add_all(companies + devs + freebies)
    session.commit()
    return companies, devs, freebies
    
print("creating relationships")
def relate_many_to_many(companies, devs, freebies):
    for freebie in freebies:
        freebie.company = rc(companies)
        freebie.dev = rc(devs)
        
    session.add_all(freebies + companies + devs)
    session.commit()
    return companies, devs, freebies
        
print("putting it all together...")
if __name__ == '__main__':
    delete_records()
    companies, devs, freebies = create_records()
    companies, devs, freebies = relate_many_to_many(companies, devs, freebies)
    print("Success!")
    