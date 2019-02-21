import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Inventory(Base):
    __tablename__ = 'inventory'

    id = Column(Integer, primary_key = True)
    name = Column(String(250), nullable = False)
    price = Column(Float)
    description = Column(String(500))


engine = create_engine('sqlite:///inventory.db')

Base.metadata.create_all(engine)
