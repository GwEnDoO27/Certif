import uuid

from db.database import Base
from sqlalchemy import JSON, Column, ForeignKey, Integer, String #type: ignore
from sqlalchemy.orm import relationship #type: ignore

class User(Base):
    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True)
    uid = Column(String(36), unique=True, default=lambda: str(uuid.uuid4()), nullable=False)
    code_maps = relationship("UserCodeMap", back_populates="user")
    code_maps_gen_aux = relationship("UserCodeGenAux", back_populates="user")
    code_journal = relationship("UserJournal", back_populates="user")


class UserCodeMap(Base):
    __tablename__ = "user_code_maps"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # Ensure this references the 'id' column
    code_map = Column(JSON, nullable=False, default={})
    user = relationship("User", back_populates="code_maps")


class UserCodeGenAux(Base):
    __tablename__ = "user_code_maps_gen_aux"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    code_map_gen_aux = Column(JSON, nullable=False)
    user = relationship("User", back_populates="code_maps_gen_aux")

class UserJournal(Base) :
    __tablename__ = "code_journal"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    journal_map = Column(JSON, nullable=False)
    user = relationship("User", back_populates="code_journal")