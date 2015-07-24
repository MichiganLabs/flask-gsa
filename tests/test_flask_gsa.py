#!/usr/bin/env python

import sys
import base64
import json

from flask import Flask
from oauth2client.client import AccessTokenInfo
from flask_gsa import GoogleServiceAccount

import pytest
from mock import Mock

from tests.conftest import app as make_app


PYTHON3 = sys.version_info[0] == 3
if PYTHON3:
    text_type = str
else:
    text_type = unicode


def base64url_decode(s):
    rem = len(s) % 4
    if rem > 0:
        s += '=' * (4 - rem)
    # if isinstance(s, text_type):
    #     s = s.encode('utf-8')
    s = base64.b64decode(s)
    return text_type(s.decode('utf-8'))


def test_get_state_unregistered_app():
    """Verify that error is raised when extension is used without registering
    an app with init_app."""
    gsa = GoogleServiceAccount('TEST')
    app = Flask(__name__)

    with pytest.raises(AssertionError):
        with app.app_context():
            gsa._get_state()


def test_init_app(app):
    gsa = GoogleServiceAccount('TEST')
    gsa.init_app(app)

    assert 'gsa' in app.extensions

    with app.app_context():
        assert gsa._get_state() is not None


def test_init_app_on_create(app):
    gsa = GoogleServiceAccount('TEST', app)

    assert 'gsa' in app.extensions

    with app.app_context():
        assert gsa._get_state() is not None


def test_multiple_apps():
    app1 = make_app()
    app2 = make_app()
    gsa = GoogleServiceAccount('TEST')
    gsa.init_app(app1)
    gsa.init_app(app2)


def test_multiple_extensions(app):
    app.config.update({
        'TEST2_PK_FILE': 'tests/data/test.p12',
        'TEST2_PK_PASSWORD': 'notasecret',
        'TEST2_EMAIL': 'test@test.com',
    })
    gsa1 = GoogleServiceAccount('TEST')
    gsa2 = GoogleServiceAccount('TEST2')

    gsa1.init_app(app)
    gsa2.init_app(app)

    assert len(app.extensions['gsa']) == 2


def test_generate_credentials(app, extension):
    scopes = [
        'https://www.googleapis.com/auth/analytics.readonly'
    ]
    with app.app_context():
        c = extension.generate_credentials(scopes)

    hdr, payload, sig = c._generate_assertion().split('.')

    data = json.loads(base64url_decode(payload))

    assert data['iss'] == app.config['TEST_EMAIL']
    assert data['scope'] == ' '.join(scopes)


def test_generate_token(app, extension):
    example_token = AccessTokenInfo('123abc', 123)
    credentials_mock = Mock()
    credentials_mock.get_access_token.return_value = example_token
    extension.generate_credentials = Mock()
    extension.generate_credentials.return_value = credentials_mock

    scopes = [
        'https://www.googleapis.com/auth/analytics.readonly'
    ]
    with app.app_context():
        data = extension.generate_token(scopes)

    assert data['token'] == '123abc'
    assert data['issued'] == data['expires'] - 123
