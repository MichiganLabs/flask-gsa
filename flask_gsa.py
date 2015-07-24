#!/usr/bin/env python

import time

from flask import current_app
from OpenSSL.crypto import load_pkcs12
from oauth2client.client import SignedJwtAssertionCredentials

__all__ = ('GoogleServiceAccount',)


class _GSAState(object):
    """Remembers configuration for the private key/email settings."""
    def __init__(self, private_key, key_password, email):
        self.private_key = private_key
        self.key_password = key_password
        self.email = email


class GoogleServiceAccount(object):
    def __init__(self, key_prefix, app=None):
        self.key_prefix = key_prefix
        if app:
            self.init_app(app)

    def init_app(self, app):
        certfile = app.config[self.key_prefix + '_PK_FILE']
        pk_password = app.config[self.key_prefix + '_PK_PASSWORD']
        email = app.config[self.key_prefix + '_EMAIL']
        with open(certfile, 'rb') as fp:
            private_key = fp.read()

        # Try to read certificate. If password is wrong, the app will fail to
        # start up.
        load_pkcs12(private_key, pk_password).get_certificate()

        state = _GSAState(private_key, pk_password, email)

        if not hasattr(app, 'extensions'):  # pragma: no cover, old flask
            app.extensions = {}
        if 'gsa' not in app.extensions:
            app.extensions['gsa'] = {}
        app.extensions['gsa'][app] = state

    def _get_state(self):
        """Gets the state for the application"""
        assert 'gsa' in current_app.extensions, \
            'The GoogleServiceAccount extension was not registered to the ' \
            'current application. Please make sure to call init_app() first.'
        return current_app.extensions['gsa'][current_app]

    def generate_credentials(self, scope):
        """Generate an OAUTH2 credentials object for the requested scope(s)

        :param scope: May be a string or list of strings """
        state = self._get_state()
        return SignedJwtAssertionCredentials(
            state.email,
            state.private_key,
            scope,
            private_key_password=state.key_password,
        )

    def generate_token(self, scope):
        credentials = self.generate_credentials(scope)
        now = int(time.time())
        token_info = credentials.get_access_token()
        return {
            'token': token_info.access_token,
            'token_type': 'Bearer',
            'issued': now,
            'expires': now + token_info.expires_in,
        }
