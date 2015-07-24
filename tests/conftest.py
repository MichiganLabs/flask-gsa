#!/usr/bin/env python

from flask import Flask
import pytest

from flask_gsa import GoogleServiceAccount


@pytest.fixture
def app():
    class Config(object):
        TEST_PK_FILE = 'tests/data/test.p12'
        TEST_PK_PASSWORD = 'notasecret'
        TEST_EMAIL = 'test@test.com'

    _app = Flask(__name__)
    _app.config.from_object(Config)

    return _app


@pytest.fixture
def extension(app):
    return GoogleServiceAccount('TEST', app)
