"""Simple web site with results."""

import json
from flask import Flask, render_template
app = Flask(__name__)


@app.route('/')
def results():
    """Result view."""
    with open('trucks.json') as f:
        trucks_results = json.load(f)

    with open('sports.json') as f:
        sports_results = json.load(f)

    return render_template('results.html',
                           trucks_results=trucks_results,
                           sports_results=sports_results)

def main():
    """Start web server."""
    app.run(host='0.0.0.0', port=8000, debug=True, threaded=True)

if __name__ == '__main__':
    main()
