#!/usr/bin/env python
# encoding: utf-8

from .extensions import db

class Project(db.Model):
    __tablename__ = 'project'

    project_id = db.Column(db.Integer, primary_key=True)
    projectname = db.Column(db.String(255), nullable=False)
    time = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return (u'{self.__class__.__name__}: {self.project_id}'.format(self=self))

class Sample(db.Model):
    __tablename__ = 'sample'

    sample_id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.project_id'), nullable=False)
    samplename = db.Column(db.String(255), nullable=False)
    barcode = db.Column(db.String(255), nullable=True)
    time = db.Column(db.DateTime, nullable=True)

    project = db.relationship('Project', backref=db.backref('samples'))

class Supportparams(db.Model):
    __tablename__ = 'supportparams'

    supportparams_id = db.Column(db.Integer, primary_key=True)
    document_path = db.Column(db.String(255), nullable=False)
    systempid = db.Column(db.String(255), nullable=True)
    systemos = db.Column(db.String(255), nullable=True)
    systemperlv = db.Column(db.String(255), nullable=True)
    systemperlexe = db.Column(db.String(255), nullable=True)
    idstring = db.Column(db.String(255), nullable=True)
    program = db.Column(db.String(255), nullable=True)
    commandline = db.Column(db.Text)
    sampleconfig_path = db.Column(db.String(255), nullable=True)
    sampleconfig = db.Column(db.Text)
    time = db.Column(db.DateTime, nullable=True)

class Datasource(db.Model):
    __tablename__ = 'datasource'

    datasource_id = db.Column(db.Integer, primary_key=True)
    supportparams_id = db.Column(db.Integer, db.ForeignKey('supportparams.supportparams_id'), nullable=False)
    runname = db.Column(db.String(255), nullable=True)
    machine = db.Column(db.String(255), nullable=True)
    rundate = db.Column(db.DateTime, nullable=True)
    document_path = db.Column(db.String(255), nullable=False)
    document_type = db.Column(db.Enum('html', 'xml', 'undefined'), nullable=False, default='html')
    server = db.Column(db.String(255), nullable=True)
    time = db.Column(db.DateTime, nullable=True)

    supportparams = db.relationship('Supportparams', backref=db.backref('datasources'))

    def __repr__(self):
        return (u'{self.__class__.__name__}: {self.runname}'.format(self=self))

class Demux(db.Model):
    __tablename__ = 'demux'

    demux_id = db.Column(db.Integer, primary_key=True)
    flowcell_id = db.Column(db.Integer, db.ForeignKey('flowcell.flowcell_id'), nullable=False)
    datasource_id = db.Column(db.Integer, db.ForeignKey('datasource.datasource_id'), nullable=False)
    basemask = db.Column(db.String(255), nullable=True)
    time = db.Column(db.DateTime, nullable=True)

    db.UniqueConstraint('flowcell', 'basemask', name='demux_ibuk_1')

    datasource = db.relationship('Datasource', backref=db.backref('demuxes'))
    datasource = db.relationship('Flowcell', backref=db.backref('demuxes'))

class Flowcell(db.Model):
    __tablename__ = 'flowcell'

    flowcell_id = db.Column(db.Integer, primary_key=True)
    flowcellname = db.Column(db.String(255), nullable=False)
    flowcell_pos = db.Column(db.Enum('A', 'B'), nullable=False)
    time_start = db.Column(db.DateTime, nullable=True)
    time_end = db.Column(db.DateTime, nullable=True)
    time = db.Column(db.DateTime)

    db.UniqueConstraint('flowcellname', name='flowcellname')

    datasource = db.relationship('Demux', backref=db.backref('flowcells'))

class Unaligned(db.Model):
    __tablename__ = 'unaligned'

    unaligned_id = db.Column(db.Integer, primary_key=True)
    sample_id = db.Column(db.Integer, db.ForeignKey('sample.sample_id'), nullable=False)
    demux_id = db.Column(db.Integer, db.ForeignKey('demux.demux_id'), nullable=False)
    lane = db.Column(db.Integer, nullable=True)
    yield_mb = db.Column(db.Integer, nullable=True)
    passed_filter_pct = db.Column(db.Numeric(10,5), nullable=True)
    readcounts = db.Column(db.Integer, nullable=True)
    raw_clusters_per_lane_pct = db.Column(db.Numeric(10,5), nullable=True)
    perfect_indexreads_pct = db.Column(db.Numeric(10,5), nullable=True)
    q30_bases_pct = db.Column(db.Numeric(10,5), nullable=True)
    mean_quality_score = db.Column(db.Numeric(10,5), nullable=True)
    time = db.Column(db.DateTime, nullable=True)

    demux = db.relationship('Demux', backref=db.backref('unaligned'))
    sample = db.relationship('Sample', backref=db.backref('unaligned'))

class Backup(db.Model):
    __tablename__ = 'backup'

    runname = db.Column(db.String(255), primary_key=True)
    startdate = db.Column(db.Date, nullable=False)
    nas = db.Column(db.String(255), nullable=True)
    nasdir = db.Column(db.String(255), nullable=True)
    starttonas = db.Column(db.DateTime, nullable=True)
    endtonas = db.Column(db.DateTime, nullable=True)
    preproc = db.Column(db.String(255), nullable=True)
    preprocdir = db.Column(db.String(255), nullable=True)
    startpreproc = db.Column(db.DateTime, nullable=True)
    endpreproc = db.Column(db.DateTime, nullable=True)
    frompreproc = db.Column(db.DateTime, nullable=True)
    analysis = db.Column(db.String(255), nullable=True)
    analysisdir = db.Column(db.String(255)    , nullable=True)
    toanalysis = db.Column(db.DateTime, nullable=True)
    fromanalysis = db.Column(db.DateTime, nullable=True)
    backup = db.Column(db.String(255), nullable=True)
    backupdir = db.Column(db.String(255), nullable=True)
    tobackup = db.Column(db.DateTime, nullable=True)
    frombackup = db.Column(db.DateTime, nullable=True)
    tape = db.Column(db.String(255), nullable=True)
    tapedir = db.Column(db.String(255), nullable=True)
    totape = db.Column(db.DateTime, nullable=True)
    fromtape = db.Column(db.DateTime, nullable=True)
