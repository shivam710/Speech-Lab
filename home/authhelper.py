import requests
from urllib.parse import quote, urlencode
import base64
import json
import time
from django.urls import reverse
from home.outlookservice import get_me

# Client ID and secret
client_id = '3fb82505-7386-4eca-a782-839d5104d670'
client_secret = 'dbS.hJtRX.0rEuV39~CSZGi5lm7iAWhw_D'

# Constant strings for OAuth2 flow
# The OAuth authority
authority = 'https://login.microsoftonline.com'

# The authorize URL that initiates the OAuth2 client credential flow for admin consent
authorize_url = '{0}{1}'.format(authority, '/common/oauth2/v2.0/authorize?{0}')

# The token issuing endpoint
token_url = '{0}{1}'.format(authority, '/common/oauth2/v2.0/token')

# The scopes required by the app
scopes = [ 'openid',
           'profile',
           'offline_access',
           'User.Read']


def loginFLOW(request, context):
    redirect_uri = 'http://localhost:8001/home/gettoken/'
    sign_in_url = get_signin_url(redirect_uri)
    logout_url = request.build_absolute_uri(reverse('home:logout'))
    access_token = get_access_token(request,redirect_uri)
    if not access_token:
        context['username'] = ''
        print('hello\n')
    else:
        user = get_me(access_token)
        username = user['userPrincipalName'].replace("@outlook.com", "")
        context['username'] = username
        print(username+'\n')

    context['sign_in_url'] = sign_in_url
    context['logout_url'] = logout_url
    return context

def get_token_from_code(auth_code, redirect_uri):
  # Build the post form for the token request
    post_data = {'grant_type': 'authorization_code',
                'code': auth_code,
                'redirect_uri': redirect_uri,
                'scope': ' '.join(str(i) for i in scopes),
                'client_id': client_id,
                'client_secret': client_secret
              }

    r = requests.post(token_url, data=post_data,)

    try:
        return r.json()
    except:
        return 'Error retrieving token: {0} - {1}'.format(r.status_code, r.text)


def get_signin_url(redirect_uri):
  # Build the query parameters for the signin url
    params = {'client_id': client_id,
              'redirect_uri': redirect_uri,
              'response_type': 'code',
              'scope': ' '.join(str(i) for i in scopes)}

    signin_url = authorize_url.format(urlencode(params))
    print(signin_url)
    return signin_url


def get_token_from_refresh_token(refresh_token, redirect_uri):
  # Build the post form for the token request
  post_data = { 'grant_type': 'refresh_token',
                'refresh_token': refresh_token,
                'redirect_uri': redirect_uri,
                'scope': ' '.join(str(i) for i in scopes),
                'client_id': client_id,
                'client_secret': client_secret
              }

  r = requests.post(token_url, data=post_data)

  try:
    return r.json()
  except:
    return 'Error retrieving token: {0} - {1}'.format(r.status_code, r.text)


def get_access_token(request, redirect_uri):
  try:
    current_token = request.session['access_token']
  except Exception as e:
      request.session['access_token'] = None
  current_token = request.session['access_token']
  try:
    expiration = request.session['token_expires']
  except Exception as e:
      request.session['token_expires'] = None
  expiration = request.session['token_expires']
  now = int(time.time())
  if not current_token:
      return current_token
  if (current_token and now < expiration):
    # Token still valid
    return current_token

  else:
    # Token expired
    refresh_token = request.session['refresh_token']
    new_tokens = get_token_from_refresh_token(refresh_token, redirect_uri)

    # Update session
    # expires_in is in seconds
    # Get current timestamp (seconds since Unix Epoch) and
    # add expires_in to get expiration time
    # Subtract 5 minutes to allow for clock differences
    expiration = int(time.time()) + new_tokens['expires_in'] - 300

    # Save the token in the session
    request.session['access_token'] = new_tokens['access_token']
    request.session['refresh_token'] = new_tokens['refresh_token']
    request.session['token_expires'] = expiration

    return new_tokens['access_token']
