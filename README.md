# JSON Keys Viewer

A lightweight JSON endpoint that serves RSA public keys in [JWK (JSON Web Key)](https://datatracker.ietf.org/doc/html/rfc7517) format, similar to Google’s OAuth2 public key endpoint.

## 🚀 Usage

1. **Start the local server:**

   ```bash
   python -m http.server 8000
   ```

2. **View the keys:**

   ```
   http://localhost:8000/keys.json
   ```

   This URL serves your current public keys in JSON format and can be viewed in any modern browser.

## 🔁 Automatic Key Rotation

To enable automatic key rotation, switch to the appropriate branch:

```bash
git checkout feature/automatic-key-rotation
```

The system rotates RSA keys every 15 minutes by default using:

```python
schedule.every(15).minutes.do(rotate_key)
```

### ⏱ To change the rotation interval:

Edit the schedule line in your rotation script. For example, to rotate every 5 minutes:

```python
schedule.every(5).minutes.do(rotate_key)
```

