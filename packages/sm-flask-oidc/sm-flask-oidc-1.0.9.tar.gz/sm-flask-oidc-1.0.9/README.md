SM Flask OIDC

This can be helpfull if you want to implement IdentityServer4 OIDC in Flask Python application
--------------------------------------------------------------

How to use:

Install: python -m pip install sm-flask-oidc
Upgrade: python -m pip install sm-flask-oidc --upgrade

Import: from sm_flask_oidc import sm_flask_oidc_helper

Define Params:
    CLIENT_ID = ''
    CLIENT_SECRET = ''
    APP_URI = ''
    AUTH_API_ROUTE = ''
    AUTH_STATE = ''

Activate Flask Session: app.secret_key = "my-super-secret"

Create instance: sm_oidc = sm_flask_oidc_helper.SmFlaskOidcHelper(CLIENT_ID, CLIENT_SECRET, APP_URI, AUTH_API_ROUTE, AUTH_STATE)

Define Required Routes:

    @app.route("/login")
    def login():
        return sm_oidc.login()

    @app.route("/login-callback")
    def login_callback():
        return sm_oidc.login_callback()

    @app.route("/logout")
    def logout():
        return sm_oidc.logout()

    @app.route("/logout-callback")
    def logout_callback():
        return sm_oidc.logout_callback()
--------------------------------------------------------------

Notes:

After login the following keys will be added to flask.session: id_token, name, email, is_authorized
