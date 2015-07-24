# Flask-GSA
A Flask extension for interacting with [Google OAuth2 Service Accounts][service-accounts].

[![Build Status][travis-badge]][build-status]
[![Coverage Status][coveralls-badge]][coveralls-status]
[![PyPI Version][pypi-version-badge]][pypi]
[![PyPI Downloads][pypi-downloads-badge]][pypi]

# Getting Started
## Requirements

* Python 2.6+
* OpenSSL

## Installation
Flask-GSA can be installed with pip:

```
$ pip install Flask-GSA
```

## Basic Usage
A minimal sample application:

```python
from flask import Flask
from flask_gsa import GoogleServiceAccount

app = Flask(__name__)

# Create a service account object and assign a config variable prefix
analytics_gsa = GoogleServiceAccount('ANALYTICS_GSA')

# Set up the service account settings
app.config['ANALYTICS_GSA_PK_FILE'] = 'analytics.p12'
app.config['ANALYTICS_GSA_PK_PASSWORD'] = 'notasecret'
app.config['ANALYTICS_GSA_EMAIL'] = '12345abcd@developer.gserviceaccount.com'

# Initialize the extension
analytics_gsa.init_app(app)

@app.route('/token')
def get_analytics_token():
    scopes = [
        'https://www.googleapis.com/auth/analytics.readonly'
    ]
    return analytics_gsa.generate_token(scopes)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
```

Run the app:

```
$ python example.py
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
```

Get a token:

```
$ http :5000/token
{
    "expires": 1437698007,
    "issued": 1437694408,
    "token": "ya29.uQEiLFkED9YMTG7CvctLYtJqnOny_8CkA4_Hxk5yxzEhXR3eNSO-Pca20BRNxBT74XYD",
    "token_type": "Bearer"
}
```

## Configuration Options:
When creating an instance of the extension, you must choose a config variable
prefix. This allows multiple service account objects to be used with the same
app:

```python
analytics_gsa = GoogleServiceAccount('ANALYTICS')
gdrive_gsa = GoogleServiceAccount('GDRIVE')
```

The following config variables are required:

| Config Variable        | Description                                             |
| ---------------------- | ------------------------------------------------------- |
| `<prefix>_PK_FILE`     | Path to the PKCS12 key that will be used to sign tokens |
| `<prefix>_PK_PASSWORD` | Password for the PKCS12 private key                     |
| `<prefix>_EMAIL`       | Service Account's email address                         |

[travis-badge]: http://img.shields.io/travis/MichiganLabs/flask-gsa/master.svg
[build-status]: https://travis-ci.org/MichiganLabs/flask-gsa
[coveralls-badge]: http://img.shields.io/coveralls/MichiganLabs/flask-gsa/master.svg
[coveralls-status]: https://coveralls.io/r/MichiganLabs/flask-gsa
[pypi-version-badge]: http://img.shields.io/pypi/v/Flask-GSA.svg
[pypi-downloads-badge]: http://img.shields.io/pypi/dm/Flask-GSA.svg
[pypi]: https://pypi.python.org/pypi/Flask-GSA
[service-accounts]: https://developers.google.com/identity/protocols/OAuth2ServiceAccount
