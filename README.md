# JSON Keys Server and Rotator

This project provides a simple JSON endpoint to serve RSA public keys in JWK format and a script to automatically rotate these keys periodically. This setup is similar to how services like Google expose their OAuth2 public keys, with the added feature of automated key rotation.

## Features

*   Serves a `keys.json` file containing RSA public keys in JWK format.
*   Includes a `key_rotator.py` script that automatically updates one key in `keys.json` every 15 minutes.
*   Keys are generated using `PyCryptodome` and scheduling is handled by `schedule`.

## Dependencies

The project requires the following Python libraries:

*   **PyCryptodome:** Used for generating RSA keys.
*   **schedule:** Used for scheduling the periodic key rotation.

You can install them using pip:
```bash
pip install PyCryptodome schedule
```

## Serving Keys

To serve the `keys.json` file, you can use Python's built-in HTTP server.

1.  Navigate to the project directory in your terminal.
2.  Start the local server:
    ```bash
    python -m http.server 8000
    ```
3.  Access the keys at:
    ```
    http://localhost:8000/keys.json
    ```
    The endpoint will return the public keys in JSON format.

## Automatic Key Rotation

The `key_rotator.py` script is responsible for automatically updating the `keys.json` file.

### Purpose
This script reads the existing `keys.json` file, randomly selects one of the keys, generates a new RSA key to replace it, and then writes the updated key set back to `keys.json`. This process is scheduled to run every 15 minutes.

### Usage
1.  Ensure you have the dependencies installed (see "Dependencies" section).
2.  Navigate to the project directory in your terminal.
3.  Run the script:
    ```bash
    python key_rotator.py
    ```
    The script will print log messages to the console, indicating when it attempts a rotation and the outcome. It will continue running to perform scheduled rotations. Press `Ctrl+C` to stop the script.

## Running the Full System

For the complete system to function (i.e., serving keys that are periodically rotated), both the HTTP server and the `key_rotator.py` script should be running simultaneously.

You can achieve this by running them in separate terminal windows:

*   **Terminal 1 (Serving Keys):**
    ```bash
    python -m http.server 8000
    ```
*   **Terminal 2 (Rotating Keys):**
    ```bash
    python key_rotator.py
    ```

This setup ensures that the `keys.json` file served by the HTTP server is periodically updated by the `key_rotator.py` script.
