"""
This script runs the StopAndSearchData application using a development server.
"""

from os import environ
from StopAndSearchData import app
from StopAndSearchData.scheduler import start_scheduler  # Import scheduler

if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    
    # Start the scheduler before running the app
    start_scheduler()
    
    app.run(HOST, PORT)