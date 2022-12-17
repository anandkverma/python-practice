from sqlalchemy import create_engine,MetaData,Integer,Float,String,Table,Column,or_
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

'''database connection url'''
DB_URL = 'mysql://root:root@localhost:3306/mydata'

'''Establishing connection with database '''
ENG = create_engine(DB_URL)

'''The Session establishes all conversations with the database. 
The session is a regular Python class which can be directly instantiated'''
Session = sessionmaker(bind=ENG)
'''bind is something that can execute SQL statements and is usually a connection or engine.'''
session = Session()

'''  declarative_base is a factory function, that returns a base class (actually a metaclass),
  and the entities are going to inherit from it.
  Once the definition of the class is done, the Table and mapper will be generated automatically.'''
Base = declarative_base()

class Customer(Base):
    __tablename__="customer"
    cid = Column( Integer, primary_key=True)
    name = Column(String(50))
    city = Column(String(40))
    age = Column(Integer)

    def __str__(self):
        return f'cid : {self.cid}, name : {self.name}, city : {self.city}, age : {self.age}'

'''create_all method is used to create a new table into the database. 
This method will first check whether the table exists in the database or not if suppose it has found an existing table it will not create any table.'''
Base.metadata.create_all(ENG)

'''data insertion in table'''
customer1 = Customer(name="anand",city="nagpur", age=29)
customer2 = Customer(name="nikhil", city="nagpur", age=28)
customer3 = Customer(name="ajit", city="nagpur", age=27)

'''to save one object at a time'''
#session.add(customer1)

'''to add multiple object in table'''
#session.add_all([customer2,customer3])#objects are passed in list form

''' commit to save changes in table '''
#session.commit()

'''Read data from table'''
customers = session.query(Customer)
for customer in customers:
    print(customer)
    print(customer.name, customer.city, customer.age)
print("---------")
'''order_by'''
customers = session.query(Customer).order_by(Customer.name)
for customer in customers:
    print(customer)

print("---------")
'''filter'''
customers = session.query(Customer).filter(Customer.name=="nikhil")
for customer in customers:
    print(customer)

print("---------")
'''filter with or_ note import 'or_' form sqlalchemy '''
customers = session.query(Customer).filter(or_(Customer.name=="nikhil",Customer.name=="anand"))
for customer in customers:
    print(customer)
print("---------")

'''Update  data in table'''
session.query(Customer).filter(Customer.name=="nikhil").update({Customer.age:29})
'''when ever changes are made commit() must be called'''
session.commit() 


'''delete data '''
customer = session.query(Customer).filter(Customer.name=="ajit")
customer.delete()
session.commit()
