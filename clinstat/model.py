#!/usr/bin/env python
# encoding: utf-8

from sqlalchemy import Boolean, Column
from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.ext.declarative_base import declarative_base

Base = declarative_base()

class Project(Base):
    __tablename__ = 'project'

    project_id = Column(Integer, primary_key=True)
    projectname = Column(String(255), nullable=False)
    time = Column(DateTime, nullable=False)


