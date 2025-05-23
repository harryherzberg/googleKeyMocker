# JSON Keys Viewer

A simple JSON endpoint that serves RSA public keys in JWK format, similar to Google's OAuth2 public keys endpoint.

## Usage

1. Start the local server:
```bash
python -m http.server 8000
```

2. Access the keys at:
```
http://localhost:8000/keys.json
```

The endpoint will return the public keys in JSON format, which can be viewed with any browser's built-in JSON viewer. 

to change the speed of the rotations (defualt 15 minutes) its     schedule.every(15).minutes+.do(rotate_key)
