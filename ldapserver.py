#!/usr/bin/python
# coding=utf-8
from flask import Flask, request, Response
from functools import wraps
from flask.ext.ldap import LDAP

app = Flask(__name__)
ldap = LDAP(app)

app.debug = True
app.config['LDAP_HOST'] = 'server.com'
app.config['LDAP_PORT'] = '389'
app.config['LDAP_SCHEMA'] = 'ldap'
# domain & search base
app.config['LDAP_DOMAIN'] = 'server.com'
app.config['LDAP_SEARCH_BASE'] = 'DC=server,DC=com'
app.config['LDAP_REQUIRED_GROUP'] = ('DC=server,DC=com')

app.secret_key = "asdf"

def authenticate():
    '''The authentication procedure if the user is not authenticated'''
    return Response("Couldn't verify your credentials.  Please try again"
                    " or contact your Systems "
                    "Administrator.", 401, {'WWW-Authenticate':
                                            'Basic realm="Login required"'})

def login_required(f):
    '''The login_required function will prompt
    a user for authentication if enabled'''
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        print (auth)
        if not auth or not ldap.ldap_login(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated
    
@app.route('/')
@login_required
def index():
        return "You have been logged in."

if __name__ == '__main__':
    app.run(debug=True, port=80, host="0.0.0.0")