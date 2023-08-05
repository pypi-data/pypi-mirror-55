from urllib.parse import urlencode

import requests


class Provider:
    def __init__(
        self,
        name,
        client_id,
        client_secret,
        access_token_url,
        authorize_url,
        redirect_url,
        user_info_url,
        scope=None,
        user_info_fields=None,
    ):
        self.name = name
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token_url = access_token_url
        self.authorize_url = authorize_url
        self.redirect_url = redirect_url
        self.user_info_url = user_info_url
        self.scope = scope
        self.user_info_fields = user_info_fields or ["email"]
        self.session = requests.Session()

    def get_authorization_url(self, state):
        params = dict(response_type="code", client_id=self.client_id, redirect_url=self.redirect_url, state=state)
        if self.scope:
            params["scope"] = self.scope

        return f"{self.authorize_url}?{urlencode(params)}"

    def get_access_token(self, code, state):
        params = dict(
            grant_type="authorization_code",
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_url=self.redirect_url,
            code=code,
            state=state,
        )
        headers = {"Accept": "application/json"}
        response = requests.post(self.access_token_url, params=params, headers=headers)
        response.raise_for_status()
        access_token_data = response.json()
        if "access_token" not in access_token_data:
            raise RuntimeError("Couldn't get access token")

        return access_token_data["access_token"]

    def get_user_info(self, access_token):
        self.session.headers["Authorization"] = f"bearer {access_token}"
        response = self.session.get(self.user_info_url)
        response.raise_for_status()
        data = {k: v for k, v in response.json().items() if k in self.user_info_fields}
        return data
