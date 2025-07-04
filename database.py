from sqlalchemy import create_engine, Integer, ForeignKey, Column, String, DateTime, Float
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timedelta
import os

def get_db_path(folder="MyAppData", filename="database.db"):
    from pathlib import Path

    base_dir = Path.home() / folder
    base_dir.mkdir(parents=True, exist_ok=True)

    return str(base_dir / filename)

print("db at: ", get_db_path())

Base = declarative_base()

engine = create_engine(f"sqlite:///{get_db_path()}", echo=False)
Session = sessionmaker(bind=engine)
session = Session()


class Product(Base):
    __tablename__ = "products"
    prod_id = Column(Integer, primary_key=True)
    prod_name = Column(String, nullable=False)
    prod_desc = Column(String, nullable=False)
    prod_category = Column(String, nullable=False)
    quantity = Column(Integer, default=0)
    prod_price = Column(Float, nullable=False, default=0)
    product_image = Column(String, nullable=False)
    date_added = Column(DateTime, default=datetime.utcnow())

    transactions = relationship("Transaction", back_populates="product")



class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True)
    user_name = Column(String, nullable=False)
    user_password = Column(String, nullable=False)
    user_role = Column(String, nullable=False)
    date_added = Column(DateTime, default=datetime.utcnow)
    
    transactions = relationship("Transaction", back_populates="user")

class Transaction(Base):
    __tablename__ = "transactions"
    trans_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    prod_id = Column(Integer, ForeignKey("products.prod_id"), nullable=False)
    receipt_id = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    date = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="transactions")
    product = relationship("Product", back_populates="transactions")


class Cylinder(Base):
    __tablename__ = "cylinders"
    cylinder_id = Column(Integer, primary_key=True)
    cylinder_name = Column(String, nullable=False) 
    cylinder_loc = Column(String, nullable=False) 
    six_kg_count = Column(Integer, default = 0) 
    thirteen_kg_count = Column(Integer, default = 0) 
    three_kg_count = Column(Integer, default = 0) 
    fifty_kg_count = Column(Integer, default = 0) 

def add_admin():
    user = session.query(User).filter_by(user_name = "admin").first()
    if not user:
        admin = User(user_name = "admin", user_password = "Al.e.lunar4", user_role = "admin")
        session.add(admin)
        session.commit()
    else:
        print("Admin Exists!!")

Base.metadata.create_all(engine)