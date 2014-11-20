# encoding: utf-8

from flask import Blueprint, url_for

from ..models import Project

core = Blueprint('core', __name__, template_folder='templates')

@core.route('/')
def index():
    return 'Projects #{}'.format(Project.query.all())


