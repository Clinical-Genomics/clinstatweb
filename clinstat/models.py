#!/usr/bin/env python
# encoding: utf-8

from sqlalchemy import Boolean, Column, ForeignKey, UniqueConstraint
from sqlalchemy import DateTime, Integer, String, Text, Numeric, Enum
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Project(Base):
    __tablename__ = 'project'

    project_id = Column(Integer, primary_key=True)
    projectname = Column(String(255), nullable=False)
    time = Column(DateTime, nullable=False)

class Sample(Base):
    __tablename__ = 'sample'

    sample_id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('Project.project_id'), nullable=False)
    samplename = Column(String(255), nullable=False)
    barcode = Column(String(255), nullable=True)
    time = Column(DateTime, nullable=True)

class Supportparams(Base):
    __tablename__ = 'supportparams'

    supportparams = Column(Integer, primary_key=True)
    document_path = Column(String(255), nullable=False)
    systempid = Column(String(255), nullable=True)
    systemos = Column(String(255), nullable=True)
    systemperlv = Column(String(255), nullable=True)
    systemperlexe = Column(String(255), nullable=True)
    idstring = Column(String(255), nullable=True)
    program = Column(String(255), nullable=True)
    commandline = Column(Text)
    sampleconfig_path = Column(String(255), nullable=True)
    sampleconfig = Column(Text)
    time = Column(DateTime, nullable=True)

class Datasource(Base):
    __tablename__ = 'datasource'

    datasource_id = Column(Integer, primary_key=True)
    supportparams_id = Column(Integer, ForeignKey('supportparams.supportparams_id'), nullable=False)
    runname = Column(String(255), nullable=True)
    rundate = Column(DateTime, nullable=True)
    document_path = Column(String(255), nullable=False)
    document_type = Column(Enum('html', 'xml', 'undefined'), nullable=False, default='html')
    server = Column(String(255), nullable=True)
    time = Column(DateTime, nullable=True)

class Flowcell(Base):
    __tablename__ = 'flowcell'

    flowcell_id = Column(Integer, primary_key=True)
    datasource_id = Column(Integer, ForeignKey('datasource.datasource_id'), nullable=False)
    flowcellname = Column(String(255), nullable=False)
    flowcell_pos = Column(Enum('A', 'B'), nullable=False)
    time_start = Column(DateTime, nullable=True)
    time_end = Column(DateTime, nullable=True)
    time = Column(DateTime)

    UniqueConstraint('flowcellname', name='flowcellname')

class Unaligned(Base):
    __tablename__ = 'unaligned'

    unaligned_id = Column(Integer, primary_key=True)
    sample_id = Column(Integer, ForeignKey('Sample.sample_id'), nullable=False)
    flowcell_id = Column(Integer, ForeignKey('Flowcell.flowcell_id'), nullable=False)
    lane = Column(Integer, nullable=True)
    yield_mb = Column(Integer, nullable=True)
    passed_filter_pct = Column(Numeric(10,5), nullable=True)
    readcounts = Column(Integer, nullable=True)
    raw_cluster_per_lane_pct = Column(Numeric(10,5), nullable=True)
    perfect_indexreads_pct = Column(Numeric(10,5), nullable=True)
    q30_bases_pct = Column(Numeric(10,5), nullable=True)
    mean_quality_score = Column(Numeric(10,5), nullable=True)
    time = Column(DateTime, nullable=True)
    
    UniqueConstraint(flowcell_id, sample_id, lane, name='unaligned_ibuk')



