import base64
from distutils.command.clean import clean
import requests

# this builds the url for the app to get the code url returns a string
def get_code_url(param_dict: dict):

    parameters = {
        "response_type": "code",
        "client_id": param_dict["client_id"],
        "scope": param_dict["scope"],
        "redirect_uri": param_dict["redirect_url"],
        "state": param_dict["state"]
    }

    url = "https://accounts.spotify.com/authorize?"
    for i, param in enumerate(parameters.items()):

        if i != 0:
            url += '&'
        
        addition = str(param[0]) + '=' + str(param[1])
        url += addition 

    return url

# builds access token request with user code
def get_token(param_dict: dict):

    url = 'https://accounts.spotify.com/api/token'
    clientString = f'{param_dict["client_id"]}:{param_dict["client_secret"]}'
    
    messageBytes = clientString.encode('ascii')
    base64Bytes = base64.b64encode(messageBytes)
    base64Message = base64Bytes.decode('ascii')
    payload = {
        'form': {
            'code': param_dict["code"],
            'redirect_uri': param_dict["redirect_url"],
            'grant_type': 'authorization_code',
            },
        'headers': {
            'Authorization': f'Basic {base64Message}',
            'Content-Type': 'application/x-www-form-urlencoded'
            },
        'json': True
        }
        
    r = requests.post(url, headers=payload['headers'], data=payload['form'])
    token = dict(r.json())

    return token

# gets top 50 tracks or artists
def user_top(token, term_choice='short', data_type='tracks'):
    
    if term_choice not in ['short', 'medium', 'long']:
        term_choice = 'short'
    
    if data_type not in ['artists', 'tracks']:
        data_type = 'tracks'

    url = f"https://api.spotify.com/v1/me/top/{data_type}?time_range={term_choice}_term&limit=50&offset=0"

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    r = requests.get(url, headers=headers)
    response = r.json()

    return response

def get_top_features(token, cleaned_track_data):

    id_list = [track['id'] for track in cleaned_track_data]
    id_string = '%2C'.join(id_list)
    url = f"https://api.spotify.com/v1/audio-features?ids={id_string}"

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    r = requests.get(url, headers=headers)
    response = r.json()
    return response

def top_tracks_cleaner(data):
	x = []
	s = data['items']

	for i in s:
		x.append({
            # might need to add semantic backup
        	'song': i['name'],   #.replace(r'[', 'u'*5).replace(r']', 'y'*5),
            'album': i['album']['name'].replace('"', "'"),
            'artists': [artist['name'] for artist in i['artists']],
            'id': i['id'],
            'popularity': i['popularity'],
            'img': i['album']['images'][0]['url']
            })
	
	return x

def top_artists_cleaner(data):
	x = []
	s = data['items']

	for i in s:
		x.append({
        	'artist': i['name'],
            'genres': i['genres'],
            'id': i['id'],
            'popularity': i['popularity'],
            'img': i['images'][0]['url']
			})
	
	return x