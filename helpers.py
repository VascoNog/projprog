import csv
import datetime
import pytz
import requests
import urllib
import uuid

from flask import redirect, render_template, request, session
from functools import wraps


# Baseado no exercício "finance" do CS50
def apology(message, code=400):
    """Render message as an apology to user."""

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
        ]:
            s = s.replace(old, new)
        return s

    return render_template("apology.html", message=message, code=code)


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function

def format_codLER(value):
    """Format code "LER" """
    # Confirm that the LER code entered is in one of the two allowed formats: XX XX XX or XXXXXX with X = digit
    if len(value) == 6 and value.isdigit():
        return f"{value[:2]} {value[2:4]} {value[4:]}"
    
    if len(value) == 8 and value[0:2].isdigit() and value[2].isspace() and value[3:5].isdigit() and value[5].isspace() and value[6:].isdigit():
        return value
    
    return None

def format_ton(value):
    """Format Ton value"""
    return f"{value:,.3f}"

# def get_year(value):
#     """Format hour"""
#     return f"{value: %Y}"




    
    
        