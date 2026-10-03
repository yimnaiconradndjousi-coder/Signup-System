from flask import render_template
from app import app

@app.route('/')
@app.route('/me')
def index():
    user = {'name':'Yimnai Conrad'}
    return  render_template('index.html', user=user)

@app.route('/user')
def user():
    name = "Yimnai conrad"
    return render_template('index.html', name=name)


