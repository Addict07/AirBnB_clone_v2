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


@app.route('/states', strict_slashes=False)
def states():
    """return list of states"""
    states = storage.all(State)
    return render_template('9-states.html',
                           instances=states.values(), h1="States")


@app.route('/states/<id>', strict_slashes=False)
def state_id(id):
    """return cities of state by id"""
    states = storage.all(State)
    if id in [state.id for state in states.values()]:
        state = states[f'State.{id}']
        return render_template('9-states.html',
                               instances=state.cities,
                               h1=f"State: {state.name}", h3="Cities")
    return render_template('9-states.html',
                           h1="Not found!")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
