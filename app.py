from flask import Flask,render_template,request,redirect
import requests,json
from requests_oauthlib import OAuth1
from urlparse import parse_qs
import urllib,webbrowser
from TwitterAPI import TwitterAPI
from requests_oauthlib import OAuth1Session
import json

app=Flask(__name__)

client_key = 'DqyOCuGkfcrsdL3jHmjiRCeoD'
client_secret = 'l6DEFRdcCKsvps483KOmne7dJ7rzYtFwaCxacQjiegbqLDjpUn'
request_token_url = 'https://api.twitter.com/oauth/request_token'
base_authorization_url = 'https://api.twitter.com/oauth/authorize'
verifier = ''
resource_owner_key = ''
resource_owner_secret = ''
tweet=''

#Open the Index Page when the Acumen Application Loads

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/authenticate')
def authenticate():
    global resource_owner_key
    global resource_owner_secret

    oauth = OAuth1Session(client_key, client_secret=client_secret,callback_uri='http://127.0.0.1:8080/home')
    fetch_response = oauth.fetch_request_token(request_token_url)

    resource_owner_key = fetch_response.get('oauth_token')
    resource_owner_secret = fetch_response.get('oauth_token_secret')

    authorization_url = oauth.authorization_url(base_authorization_url)
    return redirect(authorization_url, code=302)

@app.route('/home')
def status_update_get():
    global verifier
    verifier = request.args.get('oauth_verifier')
    return render_template('home.html')

##post Status on Twitter
@app.route('/status_update',methods=['POST'])
def status_update():
    tweet_data = request.form['status']
    global resource_owner_key
    global resource_owner_secret
    access_token_url = 'https://api.twitter.com/oauth/access_token'
    oauth = OAuth1Session(client_key,
                          client_secret=client_secret,
                          resource_owner_key=resource_owner_key,
                          resource_owner_secret=resource_owner_secret,
                          verifier=verifier)
    oauth_tokens = oauth.fetch_access_token(access_token_url)
    resource_owner_key = oauth_tokens.get('oauth_token')
    resource_owner_secret = oauth_tokens.get('oauth_token_secret')

    protected_url = 'https://api.twitter.com/1.1/statuses/update.json?status=' + tweet_data
    print protected_url
    oauth = OAuth1Session(client_key,
                          client_secret=client_secret,
                          resource_owner_key=resource_owner_key,
                          resource_owner_secret=resource_owner_secret)
    r = oauth.post(protected_url)

    return render_template('home.html')

##Unfollow User on Twitter
@app.route('/unfollow',methods=['POST'])
def unfollow():
    unfollow1 = request.form['unfollow']
    print unfollow1
    global resource_owner_key
    global resource_owner_secret
    access_token_url = 'https://api.twitter.com/oauth/access_token'
    oauth = OAuth1Session(client_key,
                          client_secret=client_secret,
                          resource_owner_key=resource_owner_key,
                          resource_owner_secret=resource_owner_secret,
                          verifier=verifier)
    oauth_tokens = oauth.fetch_access_token(access_token_url)
    resource_owner_key = oauth_tokens.get('oauth_token')
    resource_owner_secret = oauth_tokens.get('oauth_token_secret')
    protected_url = 'https://api.twitter.com/1.1/friendships/destroy.json?screen_name=' + unfollow1
    print protected_url
    oauth = OAuth1Session(client_key,
                          client_secret=client_secret,
                          resource_owner_key=resource_owner_key,
                          resource_owner_secret=resource_owner_secret)
    r = oauth.post(protected_url)

    return render_template('home.html')

#get Timeline
@app.route('/get_timeline',methods=['post'])
def get_timeline():
    global resource_owner_key
    global resource_owner_secret
    access_token_url = 'https://api.twitter.com/oauth/access_token'
    oauth = OAuth1Session(client_key,
                          client_secret=client_secret,
                          resource_owner_key=resource_owner_key,
                          resource_owner_secret=resource_owner_secret,
                          verifier=verifier)
    oauth_tokens = oauth.fetch_access_token(access_token_url)
    resource_owner_key = oauth_tokens.get('oauth_token')
    resource_owner_secret = oauth_tokens.get('oauth_token_secret')

    protected_url = 'https://api.twitter.com/1.1/statuses/home_timeline.json'
    oauth = OAuth1Session(client_key,
                          client_secret=client_secret,
                          resource_owner_key=resource_owner_key,
                          resource_owner_secret=resource_owner_secret)
    r = oauth.get(protected_url)
    rlist = json.loads(r.content)
    jsonresponse = [{"name": x["user"]["screen_name"], "tweet": x["text"]} for x in rlist]
    return render_template('home.html',output=jsonresponse)

#get Followers
@app.route('/get_followers')
def get_followers():
    global resource_owner_key
    global resource_owner_secret
    access_token_url = 'https://api.twitter.com/oauth/access_token'
    oauth = OAuth1Session(client_key,
                          client_secret=client_secret,
                          resource_owner_key=resource_owner_key,
                          resource_owner_secret=resource_owner_secret,
                          verifier=verifier)
    oauth_tokens = oauth.fetch_access_token(access_token_url)
    resource_owner_key = oauth_tokens.get('oauth_token')
    resource_owner_secret = oauth_tokens.get('oauth_token_secret')

    protected_url = 'https://api.twitter.com/1.1/followers/list.json'
    oauth = OAuth1Session(client_key,
                          client_secret=client_secret,
                          resource_owner_key=resource_owner_key,
                          resource_owner_secret=resource_owner_secret)
    r = oauth.get(protected_url)
    print r.content
    rlist = json.loads(r.content)
    jsonresponse = [{"name": x.users.screen_name, "tweet": x.users.name } for x in rlist]
    return render_template('get_followers.html',output=jsonresponse)

#get Friends
@app.route('/friends',methods=['post'])
def friends():
    global resource_owner_key
    global resource_owner_secret
    access_token_url = 'https://api.twitter.com/oauth/access_token'
    oauth = OAuth1Session(client_key,
                          client_secret=client_secret,
                          resource_owner_key=resource_owner_key,
                          resource_owner_secret=resource_owner_secret,
                          verifier=verifier)
    oauth_tokens = oauth.fetch_access_token(access_token_url)
    resource_owner_key = oauth_tokens.get('oauth_token')
    resource_owner_secret = oauth_tokens.get('oauth_token_secret')

    protected_url = 'https://api.twitter.com/1.1/friends/list.json'
    oauth = OAuth1Session(client_key,
                          client_secret=client_secret,
                          resource_owner_key=resource_owner_key,
                          resource_owner_secret=resource_owner_secret)
    r = oauth.get(protected_url)
    print r.content
    rlist = json.loads(r.content)
    jsonresponse = [{"name": x['screen_name'], "tweet": x['status']['text']} for x in rlist['users']]
    return render_template('home.html',output=jsonresponse)

#Search Tweets
@app.route('/tweets',methods=['POST'])
def tweets():
    # import json
    search_tweet = request.form['find']
    global resource_owner_key
    global resource_owner_secret
    access_token_url = 'https://api.twitter.com/oauth/access_token'
    oauth = OAuth1Session(client_key,
                          client_secret=client_secret,
                          resource_owner_key=resource_owner_key,
                          resource_owner_secret=resource_owner_secret,
                          verifier=verifier)
    oauth_tokens = oauth.fetch_access_token(access_token_url)
    resource_owner_key = oauth_tokens.get('oauth_token')
    resource_owner_secret = oauth_tokens.get('oauth_token_secret')

    protected_url = 'https://api.twitter.com/1.1/search/tweets.json?q=' + search_tweet
    oauth = OAuth1Session(client_key,
                          client_secret=client_secret,
                          resource_owner_key=resource_owner_key,
                          resource_owner_secret=resource_owner_secret)
    r = oauth.get(protected_url)
    print r.content
    rlist = json.loads(r.content)
    jsonresponse = [{"name": x['user']['screen_name'],"tweet": x['text']} for x in rlist['statuses']]
    return render_template('home.html',output=jsonresponse)

#Get Account Settings
@app.route('/settings',methods=['POST'])
def settings():
    global resource_owner_key
    global resource_owner_secret
    access_token_url = 'https://api.twitter.com/oauth/access_token'
    oauth = OAuth1Session(client_key,
                          client_secret=client_secret,
                          resource_owner_key=resource_owner_key,
                          resource_owner_secret=resource_owner_secret,
                          verifier=verifier)
    oauth_tokens = oauth.fetch_access_token(access_token_url)
    resource_owner_key = oauth_tokens.get('oauth_token')
    resource_owner_secret = oauth_tokens.get('oauth_token_secret')

    protected_url = 'https://api.twitter.com/1.1/account/settings.json'
    oauth = OAuth1Session(client_key,
                          client_secret=client_secret,
                          resource_owner_key=resource_owner_key,
                          resource_owner_secret=resource_owner_secret)
    r = oauth.get(protected_url)
    rlist = json.loads(r.content)
    jsonresponse = [{"name": rlist["screen_name"],"lang": rlist["language"],"cookie":rlist["use_cookie_personalization"]}]
    return render_template('home.html',output1=jsonresponse)


if __name__ == '__main__':
    app.run(host='127.0.0.1',port=8080,debug=True)