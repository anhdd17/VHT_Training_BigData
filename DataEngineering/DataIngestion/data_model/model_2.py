from sqlalchemy import Column, String, ForeignKey, DateTime, text, func
from sqlalchemy.orm import relationship
from config.db_config import Base

class SI(Base):
    __tablename__ = "si"
    si_id = Column(String, primary_key=True, index=True)
    si_name = Column(String)

    group = relationship("Group", back_populates="si")

class Group(Base):
    __tablename__ = "groups"
    group_id = Column(String, primary_key=True, index=True)
    group_name = Column(String)
    si_id = Column(String, ForeignKey('si.si_id', name='si_fk'))

    si = relationship("SI", back_populates="group")

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    group_id = Column(String, ForeignKey('groups.group_id', name='group_fk'))
    role = Column(String, default="user")


class AI_Tag(Base):
    __tablename__ = "ai_tags"
    tag_id = Column(String, primary_key=True, index=True)
    tag_name = Column(String)

    ai_models = relationship("AI_Model", back_populates="ai_tags")



class AI_Model(Base):
    __tablename__ = "ai_models"
    ai_model_id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey('users.id', name='user_fk'))
    tag_id = Column(String, ForeignKey('ai_tags.tag_id', name='ai_tag_fk'))
    created_date = Column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    ai_domain = Column(String)
    library = Column(String)
    updated_date = Column(DateTime, onupdate=func.now())
    updated_by_user = Column(String)

    ai_model_cards = relationship("Model_Card", back_populates="ai_models")
    ai_tags = relationship("AI_Tag", back_populates="ai_models")
    

class Model_Card(Base):
    __tablename__ = "model_cards"
    ai_model_card_id = Column(String, primary_key=True, index=True)
    ai_model_id = Column(String, ForeignKey('ai_models.ai_model_id', name='ai_model_fk'))
    created_date = Column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    path_storage = Column(String)
    bucket = Column(String)

    ai_models = relationship("AI_Model", back_populates="model_cards")
