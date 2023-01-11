import requests
import json

REDIRECT_URI  = ""
CLIENT_ID     = ""
CLIENT_SECRET = ""

def _parse_file(filename):
    
    credentials = json.loads( open(filename, "r").read() )

    assert "web" in credentials.keys(), "Invalid OAUTH Type used, must be 'web'"
    assert set(['client_id', 'client_secret', 'redirect_uris']).issubset(credentials["web"].keys()), "missing credential params"
    
    REDIRECT_URI  = credentials["web"]['redirect_uris'][0]
    CLIENT_ID     = credentials["web"]['client_id']
    CLIENT_SECRET = credentials["web"]['client_secret']

    return (REDIRECT_URI, CLIENT_ID, CLIENT_SECRET)



def get_link(scopes, credentials=""):

    if credentials:
        REDIRECT_URI, CLIENT_ID, CLIENT_SECRET = _parse_file(credentials)

    # encode 'scope'
    # encode 'redirect_uri'
    # Actual Link below 
        # approval_prompt=force&
    link = f'''
    https://accounts.google.com/o/oauth2/v2/auth?
    scope={"%20".join(scopes).replace(":", "%3A")}&
    prompt=consent&
    access_type=offline&
    include_granted_scopes=true&
    response_type=code&
    state=state_parameter_passthrough_value&
    redirect_uri={REDIRECT_URI.replace(":", "%3A")}&
    client_id={CLIENT_ID}
    '''

    return link

def init(oauth_result):

    # Parse OAUTH return link
    oauth_result = oauth_result.split("?")[1].split("&")
    code = oauth_result[1].split("=")[1].replace("%2F", "/")

    assert REDIRECT_URI  != "", "REDIRECT_URI is empty"
    assert CLIENT_ID     != "", "CLIENT_ID is empty"
    assert CLIENT_SECRET != "", "CLIENT_SECRET is empty"

    resp = requests.post(
        url="https://oauth2.googleapis.com/token",
        json={
            'code'         : code,
            'client_id'    : CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'redirect_uri' : REDIRECT_URI,
            'grant_type'   : 'authorization_code',
            }
    )

    assert resp.status_code == 200, json.dumps(resp.json(),indent=2)

    return resp.json()

def refresh(refresh_token):

    # Assert params are set
    assert REDIRECT_URI  != "", "REDIRECT_URI is empty"
    assert CLIENT_ID     != "", "CLIENT_ID is empty"
    assert CLIENT_SECRET != "", "CLIENT_SECRET is empty"

    # get access token from refresh
    resp = requests.post(
        url="https://oauth2.googleapis.com/token",
        json={
            'client_id'    : CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'redirect_uri' : REDIRECT_URI,
            'grant_type'   : 'refresh_token',
            'refresh_token': refresh_token
            }
    )

    assert resp.status_code == 200, json.dumps(resp.json(),indent=2)

    return resp.json()