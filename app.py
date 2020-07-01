from flask import Flask, redirect, url_for, session
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)
app.secret_key = 'random secret'

# oauth config
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id='<PUT YOUR ID>',
    client_secret='<PUT YOUR SECRET>',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',
    # This is only needed if using openId to fetch user info
    client_kwargs={'scope': 'openid email profile'},
)


@app.route('/')
def hello_world():
    # email = dict(session).get('email', None)
    # return f'Hello, you are logged in as {email}!'
    user = dict(session).get('user', None)
    # return f'Details: Name= {user["name"]} Email= {user["email"]} Verified Email= {user["verified_email"]}'
    return f'Details: {user}'


@app.route('/login')
def login():
    google = oauth.create_client('google')
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)


@app.route('/authorize')
def authorize():
    google = oauth.create_client('google')
    token = google.authorize_access_token()
    resp = google.get('userinfo')
    user_info = resp.json()
    print(user_info)
    # do something with the token and profile
    # session['email'] = user_info['email']
    session['user'] = user_info
    return redirect('/')


@app.route('/logout')
def logout():
    for key in list(session.keys()):
        session.pop(key)
    return redirect('/')
