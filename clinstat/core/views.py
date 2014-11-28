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
    """SELECT YEAR(rundate) AS year, MONTH(rundate) AS month, COUNT(DISTINCT datasource.datasource_id) AS runs, ROUND(SUM(readcounts/2000000),2) AS 'Mil reads'
    FROM datasource
    LEFT JOIN flowcell ON datasource.datasource_id = flowcell.datasource_id
    LEFT JOIN unaligned ON unaligned.flowcell_id = flowcell.flowcell_id
    GROUP BY YEAR(rundate), MONTH(rundate)
    ORDER BY YEAR(rundate), MONTH(rundate);"""
    rs = db.session.query(
                db.func.year(Datasource.rundate),\
                db.func.month(Datasource.rundate),\
                db.func.count(Datasource.datasource_id.distinct()),\
                db.func.round(db.func.sum(Unaligned.readcounts / 20000000), 2)
            ).\
            join(Flowcell).\
            join(Unaligned).\
            group_by(db.func.year(Datasource.rundate), db.func.month(Datasource.rundate)).\
            order_by(db.func.year(Datasource.rundate).desc(), db.func.month(Datasource.rundate).desc()).\
            all()

    return dict(out=rs)
