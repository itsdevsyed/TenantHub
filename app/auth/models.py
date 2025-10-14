from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, false
from sqlalchemy.orm import relationship , declarative_base
from sqlalchemy.sql import func
from sqlalchemy import DateTime

Base = declarative_base()

class Tenant(Base):
    __tablename__  = "tenants"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    users = relationship("User", back_populates="tenant")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=false())


    tenant = relationship("Tenant", back_populates="users")
