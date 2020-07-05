"""
This script runs the YouTube_Tag_Analysis application using a development server.
"""

from os import environ
from YouTube_Tag_Analysis import app

if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '1818'))
    except ValueError:
        PORT = 1818
    
    app.run(host='localhost', port=1818)
#    app.run(HOST, PORT)


      