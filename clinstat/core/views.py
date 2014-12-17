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
            outerjoin(Flowcell).\
            outerjoin(Unaligned).\
            group_by(db.func.year(Datasource.rundate), db.func.month(Datasource.rundate)).\
            order_by(db.func.year(Datasource.rundate).desc(), db.func.month(Datasource.rundate).desc(), db.func.day(Datasource.rundate).desc()).\
            all()

    return dict(out=rs)

@core.route('/q30')
@templated('q30.html')
def q30():
    """ SELECT runname, COUNT(DISTINCT datasource.datasource_id) AS runs,
    flowcellname, lane, SUM(readcounts),
    ROUND(SUM(readcounts)/(2000000),1) AS "mil reads/fc lane",
    GROUP_CONCAT(q30_bases_pct*readcounts), datasource.datasource_id, rundate
    FROM datasource
    LEFT JOIN flowcell ON datasource.datasource_id = flowcell.datasource_id
    LEFT JOIN unaligned ON unaligned.flowcell_id = flowcell.flowcell_id
    GROUP BY unaligned.flowcell_id, lane
    ORDER BY rundate, flowcellname, lane """
    rs = db.session.query(
            Datasource.runname,\
            db.func.count(Datasource.datasource_id.distinct()).label('runs'),\
            Flowcell.flowcellname,\
            Unaligned.lane,\
            db.func.sum(Unaligned.readcounts),\
            db.func.round(db.func.sum(Unaligned.readcounts)/(2000000), 1).label('mil reads fc lane'),\
            db.func.group_concat(Unaligned.q30_bases_pct*Unaligned.readcounts),\
            Datasource.datasource_id,\
            Datasource.rundate\
        ).\
        outerjoin(Flowcell).\
        outerjoin(Unaligned).\
        group_by(Unaligned.flowcell_id, Unaligned.lane).\
        order_by(Datasource.rundate, Flowcell.flowcellname, Unaligned.lane).\
        all()

    rows = []
    for row in rs:
        q30joined = row[6].split(',')
        q30sum = 0
        for q30s in q30joined:
            q30sum += float(q30s)
        if int(row[4]) > 0:
            fcq30 = q30sum/int(row[4])
        else:
            fcq30 = 0
        rows.append( 
            (row[8], row[0], row[1], row[2], row[3], row[4], row[5], "{0:.2f}".format(fcq30), row[7], "{0:.2f}".format(float(row[5])*float(fcq30)/100) )
        )

    return dict(out=rows)



