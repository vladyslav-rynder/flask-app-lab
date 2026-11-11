from flask import Blueprint, abort, redirect, render_template, request, url_for

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def main():
    return render_template('index.html')

@main_bp.route('/homepage')
def home():
    agent = request.user_agent
    return render_template('homepage.html', agent=agent)