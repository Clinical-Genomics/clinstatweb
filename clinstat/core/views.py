# encoding: utf-8

from __future__ import absolute_import, unicode_literals

from flask import Blueprint, url_for
from flask.ext.sqlalchemy import get_debug_queries

from ..extensions import db
from ..models import Project, Datasource, Flowcell, Unaligned
from ..helpers import templated

core = Blueprint('core', __name__, template_folder='templates')

@core.route('/projects')
def index():
    return 'Projects #{}'.format(Project.query.all())

@core.route('/')
@templated('runs.html')
def runs():
    """SELECT YEAR(rundate) AS year, MONTH(rundate) AS month, COUNT(DISTINCT datasource.datasource_id) AS runs,
    ROUND(SUM(readcounts)/2000000, 2) AS "mil reads",
    ROUND(SUM(readcounts)/(2000000*COUNT(DISTINCT datasource.datasource_id)),1) AS "mil reads/fc lane"
    FROM datasource
    LEFT JOIN flowcell ON datasource.datasource_id = flowcell.datasource_id
    LEFT JOIN unaligned ON unaligned.flowcell_id = flowcell.flowcell_id
    GROUP BY YEAR(rundate), MONTH(rundate)
    ORDER BY YEAR(rundate), MONTH(rundate), DAY(rundate); """
    rs = db.session.query(
                db.func.year(Datasource.rundate).label('year'),\
                db.func.month(Datasource.rundate).label('month'),\
                db.func.count(Datasource.datasource_id.distinct()).label('runs'),\
                db.func.round(db.func.sum(Unaligned.readcounts / 2000000), 2).label('mil reads'),\
                db.func.round(db.func.sum(Unaligned.readcounts) / (db.func.count(Datasource.datasource_id.distinct())*2000000), 1).label('mil reads fc lane')
            ).\
            join(Flowcell).\
            join(Unaligned).\
            group_by(db.func.year(Datasource.rundate), db.func.month(Datasource.rundate)).\
            order_by(db.func.year(Datasource.rundate).desc(), db.func.month(Datasource.rundate).desc(), db.func.day(Datasource.rundate).desc()).\
            all()

    return dict(out=rs)
