# RE-RE-WRAPPED
spotify rewrapped project v2
---

This project is a retry of an older project: https://github.com/tyler-sanzo/spotify_rewrapped

Goals
---

The goal for this application is to give the user a way to check their general listening history in an intuitive way.
Interfacing with Spotify's developer API, this app can grab and display someone's top tracks within a certain time-frame (as dictated by Spotify)

Tech
---

This app was built primarily in Python. Flask handles the web-app framework and the Python Requests module is used to handle api calls. Minimal data cleaning is done in Python just before it is sent as JSON to JavaScript where it is parsed and displayed.

Reason + Acknowlegement
---

Much of the work done figuring out how to go about this stuff was done in v1 with a lot of help from my group:

[Tyler Sanzo](https://github.com/tyler-sanzo)
[Alex Huynh](https://github.com/alexhuynh0530)
[Sean Draper](https://github.com/SeanDraper)
[Ariel Griffin](https://github.com/griffindex)

The reason I recreated the app was to fix some of the inconsistencies we were getting using an api interface module. I recreated the calls in my own interface. You can see how i did that in the api_handlers.py file. I just simplified the api_call down to the most basic components and built in a little bit of customization.