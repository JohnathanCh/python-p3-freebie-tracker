from sqlalchemy import ForeignKey, Column, Integer, String, MetaData, Table
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
# from debug import session

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)

engine = create_engine('sqlite:///freebies.db')
Session = sessionmaker(bind=engine)
session = Session()

# freebies = Table(
#     'freebies',
#     Base.metadata,
#     Column('dev_id', ForeignKey('dev.id'), primary_key=True),
#     Column('company_id', ForeignKey('company.id'), primary_key=True),
#     extend_existing=True
#     )

class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    founding_year = Column(Integer())
    
    freebies = relationship('Freebie', backref=backref('company'))
    devs = association_proxy('freebies', 'dev', creator=lambda d: Freebie(dev=d))

    def __repr__(self):
        return f'<Company {self.name}>'
    
    def give_freebie(self, dev, item_name, value):
        freebie = Freebie(dev=dev, item_name=item_name, value=value, company_id=self.id)
        session.add(freebie)
        session.commit()
    
    @classmethod
    def oldest_company(cls):
        return session.query(cls).order_by(cls.founding_year.asc()).first()
        

class Dev(Base):
    __tablename__ = 'devs'

    id = Column(Integer(), primary_key=True)
    name= Column(String())
    
    freebies = relationship('Freebie', backref=backref('dev'))
    companies = association_proxy('freebies', 'company', creator=lambda co: Freebie(company=co))
    
    def received_one(self,item):
        for freebie in self.freebies:
            if freebie.item_name == item:
                return True
        return False
    
    def give_away(self, other_dev, freebie):
        if freebie in self.freebies:
            freebie.dev = other_dev
            return f"{freebie.item_name} now belongs to {other_dev.name}"
        else:
            return "Aye! Did you steal that!?"

    def __repr__(self):
        return f'<Dev {self.name}>'
    
class Freebie(Base):
    __tablename__ = 'freebies'
    
    id = Column(Integer(), primary_key=True)
    item_name = Column(String())
    value = Column(Integer())
    company_id = Column(Integer(), ForeignKey('companies.id'))
    dev_id = Column(Integer(), ForeignKey('devs.id'))
    
    def __repr__(self):
        return f"Freebie(id={self.id}), " + \
            f"item_name={self.item_name}, " + \
            f"value={self.value}, " + \
            f"company={self.company_id}, " + \
            f"dev={self.dev_id}"
            
    def print_details(self):
        dev = session.query(Dev).filter(Dev.id == self.dev.id)
        return f"{self.dev.name} owns a {self.item_name} from {self.company.name}"
        
        
        
