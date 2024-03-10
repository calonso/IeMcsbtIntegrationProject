# python-oracledb demo of SQLAlchemy 2.0

import os
import datetime

import oracledb

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Identity, create_engine, select, join
from sqlalchemy.pool import NullPool
from sqlalchemy.orm import relationship, backref, sessionmaker, declarative_base

un = '<username>'
pw = '<password>'
hostname, service_name = ["<hostname from connection string>", "<service_name from connection string>"]
port = 1521

"""
# Standalone connection
engine = create_engine(
    f'oracle+oracledb://{un}:{pw}@',
    thick_mode=None,
    connect_args={
        "host": hostname,
        "port": port,
        "service_name": service_name
    }
)
"""

pool = oracledb.create_pool(user=un, password=pw,
                            dsn=dsn)

engine = create_engine("oracle+oracledb://", creator=pool.acquire, poolclass=NullPool)

# The base class which our objects will be defined on.
Base = declarative_base()

# Our User object, mapped to the 'users' table
class User(Base):
    __tablename__ = 'users'

    # Every SQLAlchemy table should have a primary key named 'id'
    id = Column(Integer, Identity(start=1), primary_key=True)

    name = Column(String(20))
    
    # Print out a user object
    def __repr__(self):
       return f"User(name='{self.name}')"

# The Address object stores the addresses of a user in the 'adressess' table.
class Address(Base):
    __tablename__ = 'addresses'

    id = Column(Integer, Identity(start=1), primary_key=True)
    email_address = Column(String(20), nullable=False)

    # Since we have a 1:n relationship, we need to store a foreign key
    # to the users table.
    user_id = Column(Integer, ForeignKey('users.id'))

    # Defines the 1:n relationship between users and addresses.
    # Also creates a backreference which is accessible from a User object.
    user = relationship("User", backref=backref('addresses'))

    # Print out an address object
    def __repr__(self):
        return f"Address(email_address='{self.email_address}')"

# Delete tables from previous runs
# Base.metadata.drop_all(engine)

# Create all tables by issuing CREATE TABLE commands to the DB.
Base.metadata.create_all(engine)

# Create a session to the database
Session = sessionmaker(bind=engine)
session = Session()

# Create a user and add two e-mail addresses to that user
ed_user = User(name='ed')
ed_user.addresses = [Address(email_address='ed@google.com'), Address(email_address='e25@yahoo.com')]

# Add the user and its addresses we've created to the DB and commit.
session.add(ed_user)
session.commit()

# Check the users and addresses in the tables
print("All users:", session.execute(select(User)).fetchall())
print("All addresses:", session.execute(select(Address)).fetchall())

# Query the user that has the e-mail address ed@google.com
sql = select(User) \
    .select_from(join(User, Address)) \
    .where(Address.email_address == 'ed@google.com')

user_by_email = session.execute(sql).fetchone()

print(user_by_email)