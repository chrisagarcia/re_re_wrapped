from flask import Flask, request, redirect, render_template
from datetime import datetime as dt
import os
from api_handlers import get_code_url, get_token, top_artists_cleaner, top_tracks_cleaner, user_top

# set up for both local and heroku
app = Flask(__name__)
state = int(dt.utcnow().timestamp())
scope = 'user-top-read user-read-recently-played user-library-read'


# local / heroku specific setup
if os.environ.get("CLIENT_SECRET"):
    client_id=os.environ['CLIENT_ID']
    client_secret=os.environ['CLIENT_SECRET']
    redirect_url = 'https://spotify-rewrapped-v2.herokuapp.com/'
else:
    from keys import client_id, client_secret
    port = 5000
    redirect_url = f"http://127.0.0.1:{port}"
    app.debug = True
    app.port = port
    print(state)
    

# necessary info for the api
spotify_api_params = {
    "client_id": client_id,
    "client_secret": client_secret,
    "redirect_url": redirect_url,
    "scope": scope,
    "state": state,
    "code": "",
    "token": {}
}

@app.route('/')
def home():

    if request.args.get('code'):

        spotify_api_params["code"] = request.args["code"]
        
        if not spotify_api_params["token"]:
            token = get_token(spotify_api_params)
            # spotify_api_params["token"] = token
            return redirect(f"/data/{token['access_token']}")

        

    return f"<a href='{get_code_url(spotify_api_params)}'>login</a>"

# possibly unsafe
@app.route('/data/<token>')
def user_data(token):

    if not token:
        return redirect('/')
    

    track_data = top_tracks_cleaner(
        user_top(
            token,
            term_choice="short",
            data_type="tracks"
            )
        )
        
    artist_data = top_artists_cleaner(
        user_top(
            token,
            term_choice="short",
            data_type="artists"
            )
        )

    return render_template("data_render.html", tracks=track_data, artists=artist_data)

if __name__ == "__main__":
    app.run()