#!/usr/bin/python3
"""
Launch a FLask App
"""

from models import storage
from models.state import State
from flask import Flask, render_template
app = Flask(__name__)


@app.teardown_appcontext
def close_session(error):
    """After each request you must remove the current Session"""
    storage.close()


@app.route('/cities_by_states', strict_slashes=False)
def cities():
    """return cities by state page"""
    states = storage.all(State)
    return render_template('8-cities_by_states.html', states=states)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
