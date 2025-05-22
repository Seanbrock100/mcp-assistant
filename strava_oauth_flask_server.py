from flask import Flask, redirect, request
import requests
import os

app = Flask(__name__)

CLIENT_ID = os.getenv("STRAVA_CLIENT_ID")
CLIENT_SECRET = os.getenv("STRAVA_CLIENT_SECRET")
REDIRECT_URI = "http://localhost:5000/exchange_token"

@app.route("/")
def index():
    return redirect(f"https://www.strava.com/oauth/authorize?client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}&approval_prompt=force&scope=read,activity:read")

@app.route("/authorize")
def authorize():
    return redirect(f"https://www.strava.com/oauth/authorize?client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}&approval_prompt=force&scope=read,activity:read")

@app.route("/exchange_token")
def exchange_token():
    code = request.args.get("code")
    if not code:
        return "Authorization code missing", 400

    response = requests.post("https://www.strava.com/api/v3/oauth/token", data={
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": code,
        "grant_type": "authorization_code"
    })

    if response.status_code == 200:
        tokens = response.json()
        return f"""
        <h2>Token Exchange Successful!</h2>
        <pre>{tokens}</pre>
        <p><strong>Access Token:</strong> {tokens.get('access_token')}</p>
        <p><strong>Refresh Token:</strong> {tokens.get('refresh_token')}</p>
        <p><strong>Expires At:</strong> {tokens.get('expires_at')}</p>
        """
    else:
        return f"<h2>Error:</h2><pre>{response.text}</pre>", 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
