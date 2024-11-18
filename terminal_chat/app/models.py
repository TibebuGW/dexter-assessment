from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime, Integer, String, ForeignKey, Table, func
from sqlalchemy.orm import relationship

Base = declarative_base()

# Users Table
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    groups = relationship("Group", secondary="group_members", back_populates="members")


# Messages Table
class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey("users.id"))
    receiver_id = Column(Integer, ForeignKey("users.id"))
    content = Column(String, index=True)
    timestamp = Column(DateTime, server_default=func.now())
    sender = relationship("User", foreign_keys=[sender_id])
    receiver = relationship("User", foreign_keys=[receiver_id])

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
