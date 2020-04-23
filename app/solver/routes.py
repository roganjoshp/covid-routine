from flask import request, jsonify, render_template, redirect, url_for

from app import db

from app.solver import bp

from flask_login import login_required

