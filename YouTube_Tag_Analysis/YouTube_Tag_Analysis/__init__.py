"""
The flask application package.
"""

from flask import Flask
app = Flask(__name__)
app.secret_key = b"85\xf9\x80'\xdd\x95\xf5\x99\xf1\\!i\xed\xd0q"
import YouTube_Tag_Analysis.views
