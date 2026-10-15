from flask import abort, redirect, render_template, request, url_for
from app import app

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/homepage')
def home():
    """View for the Home page of your website."""
    agent = request.user_agent
    return render_template('homepage.html', agent=agent)