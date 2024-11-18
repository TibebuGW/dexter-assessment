from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship

Base = declarative_base()

# Users Table
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

# Messages Table
class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    recipient_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # For 1-1 chat
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=True)  # For group chat
    content = Column(String, nullable=False)

# Groups Table
class Group(Base):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    members = relationship("User", secondary="group_members", back_populates="groups")

# Association Table for Group Members
group_members = Table(
    "group_members",
    Base.metadata,
    Column("group_id", Integer, ForeignKey("groups.id")),
    Column("user_id", Integer, ForeignKey("users.id"))
)
