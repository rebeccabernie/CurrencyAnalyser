"""
Backend Template

Use this to display server debugging info during development

"""
import os
from flask import render_template
from app.api import api_bp

@api_bp.route('/')
def api():
    return render_template('api.html', msg="Some text here")
