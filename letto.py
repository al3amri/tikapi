import requests
from bs4 import BeautifulSoup
from datetime import datetime
from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def home():
    return '<h1>Welcome to TikTok user info</h1>'

@app.route('/info')
def get_info():
    username = request.args.get('username')
    if not username:
        return '<h1>Please provide a TikTok username.</h1>'

    headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"}
    r = requests.get(f"https://www.tiktok.com/@{username}", headers=headers)
    server_log = str(r.text)

    soup = BeautifulSoup(server_log, 'html.parser')
    script = soup.find(id='SIGI_STATE').contents
    data = str(script).split('},"UserModule":{"users":{')[1]
    data_json = data
    userID = data.split('"id":"')[1].split('",')[0]
    name = data.split(',"nickname":"')[1].split('",')[0]
    secID = data.split(',"secUid":"')[1].split('"')[0]
    followers = data.split('"followerCount":')[1].split(',')[0]
    following = data.split('"followingCount":')[1].split(',')[0]
    likes = data.split('"heartCount":')[1].split(',')[0]
    videoCount = data.split('"videoCount":')[1].split(',')[0]
    signature = data.split('"signature":')[1].split(',')[0]
    region = data.split('"region":"')[1].split('"')[0]


    checkverified = data.split('"verified":')[1].split(',')[0]
    checkprivate = data.split('"privateAccount":')[1].split(',')[0]
    time = data.split('"nickNameModifyTime":')[1].split(',')[0]
    lastchangeuser = datetime.fromtimestamp(int(time))

    url_id = int(userID)

    binary = "{0:b}".format(url_id)
    i = 0
    bits = ""
    while i < 31:
        bits += binary[i]
        i += 1
    timestamp = int(bits, 2)
    dt_object = datetime.fromtimestamp(timestamp)

    info = f"<h1>TikTok user info for @{username}</h1>"
    info += f"<p>UserID: {userID}</p>"
    info += f"<p>Nickname: {name}</p>"
    info += f"<p>Bio: {signature}</p>"
    info += f"<p>Verified: {checkverified}</p>"
    info += f"<p>Private: {checkprivate}</p>"
    info += f"<p>secUid: {secID}</p>"
    info += f"<p>Followers: {followers}</p>"
    info += f"<p>Following: {following}</p>"
    info += f"<p>Likes: {likes}</p>"
    info += f"<p>Total videos: {videoCount}</p>"
    info += f"<p>User create time: {dt_object}</p>"
    info += f"<p>Last time change nickname: {lastchangeuser}</p>"
    info += f"<p>Account region: {region}</p>"
    
    return info



if __name__ == '__main__':
    app.run(debug=True)
