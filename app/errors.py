from app import app
from flask import render_template, flash, redirect, url_for, jsonify


@app.errorhandler(403)
def forbidden_error(error):
    return render_template('403.html'), 403


@app.errorhandler(500)
def internal_server_error(error):
    return render_template('500.html'), 500


