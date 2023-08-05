import json
from urllib.parse import urlencode

from beaker.middleware import SessionMiddleware
from bottle import abort, redirect, request, response
from nacl.encoding import URLSafeBase64Encoder
from nacl.signing import SigningKey

SESSION_OPTS = {"session.type": "file", "session.data_dir": "./data", "session.auto": True}


class Server:
    def __init__(self, app, sigining_key=None):
        self.__providers = {}
        self.app = SessionMiddleware(app, SESSION_OPTS)
        self.sigining_key = sigining_key or SigningKey.generate()
        self.__initialize(app)

    def __initialize(self, app):
        app.route("/authorize", ["GET"], self.authorize)
        app.route("/callback", ["GET"], self.callback)
        app.route("/info", ["GET"], self.info)

    def provider_add(self, provider):
        self.__providers[provider.name] = provider

    def provider_delete(self, name):
        self.__providers.pop(name, None)

    @property
    def providers(self):
        return list(self.__providers.keys())

    @property
    def verify_key(self):
        return self.sigining_key.verify_key.encode(encoder=URLSafeBase64Encoder).decode()

    @property
    def session(self):
        return request.environ.get("beaker.session")

    @property
    def current_provider(self):
        provider = self.session.get("provider")
        if provider and provider in self.providers:
            return self.__providers.get(provider)
        else:
            return abort(400, f"Provider {provider} is not supported")

    def info(self):
        response.content_type = "application/json"
        data = dict(verify_key=self.verify_key, providers=self.providers)
        return json.dumps(data)

    def authorize(self):
        state = request.query.get("state")
        provider = request.query.get("provider")
        redirect_url = request.query.get("redirect_url")

        # save state, provider and redirect url in session
        self.session["state"] = state
        self.session["provider"] = provider
        self.session["redirect_url"] = redirect_url

        # redirect user to provider url
        rurl = self.current_provider.get_authorization_url(state=state)
        return redirect(rurl)

    def callback(self):
        code = request.query.get("code")
        state = request.query.get("state")

        # validate the state
        if state != self.session.get("state"):
            return abort(400, "Invalid session")

        # get user info
        access_token = self.current_provider.get_access_token(code, state)
        userinfo = self.current_provider.get_user_info(access_token)

        # generate signature
        payload = urlencode(dict(state=state, **userinfo)).encode()
        signature = self.sigining_key.sign(payload, encoder=URLSafeBase64Encoder).decode()

        # redirect user to the redirect url
        redirect_url = self.session.get("redirect_url")
        rurl = f"{redirect_url}?signature={signature}"
        return redirect(rurl)
