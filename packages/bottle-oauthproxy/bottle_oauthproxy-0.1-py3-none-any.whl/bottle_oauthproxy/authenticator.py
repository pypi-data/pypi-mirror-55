import uuid
from functools import wraps
from urllib.parse import parse_qsl, urlencode

from beaker.middleware import SessionMiddleware
from bottle import abort, redirect, request, response
from nacl.encoding import URLSafeBase64Encoder
from nacl.signing import VerifyKey

SESSION_OPTS = {"session.type": "file", "session.data_dir": "./data", "session.auto": True}


class Authenticator:
    def __init__(self, app, client, login_endpoint):
        self.app = SessionMiddleware(app, SESSION_OPTS)
        self.client = client
        self.login_endpoint = login_endpoint
        self.verify_key = VerifyKey(self.client.verify_key.encode(), encoder=URLSafeBase64Encoder)

    @property
    def session(self):
        return request.environ.get("beaker.session")

    @property
    def next_url(self):
        return self.session.get("next_url", "/")

    def login(self, provider, redirect_url):
        state = str(uuid.uuid4())
        self.session["state"] = state

        # redirect user to oauth proxy
        params = dict(provider=provider, state=state, redirect_url=redirect_url)
        rurl = f"{self.client.url}/authorize?{urlencode(params)}"
        return redirect(rurl)

    def callback(self):
        signature = request.query.get("signature")
        try:
            payload = self.verify_key.verify(signature.encode(), encoder=URLSafeBase64Encoder)
            data = dict(parse_qsl(payload.decode()))
            state = data.pop("state")
            if state != self.session.get("state"):
                return abort(401, "Unauthorized")
        except:
            return abort(401, "Invalid signature")

        self.session["authotized"] = True
        return data

    def login_required(self, func):
        @wraps(func)
        def decorator(*args, **kwargs):
            if not self.session.get("authotized", False):
                self.session["next_url"] = request.path
                return redirect(self.login_endpoint)
            return func(*args, **kwargs)

        return decorator
