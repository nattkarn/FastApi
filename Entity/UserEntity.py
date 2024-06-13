from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    name = Column(String)
    password = Column(String)
    is_active = Column(Boolean, default=False)

    profile = relationship("Profile", back_populates="owner")



class Profile(Base):
    __tablename__ = "profile"

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String)
    line = Column(String)
    profileId = Column(Integer, ForeignKey("user.id"))

    owner = relationship("User", back_populates="profile")