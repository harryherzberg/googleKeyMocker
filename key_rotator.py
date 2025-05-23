import json
import random
import string
import base64
import time # Added for scheduler
import schedule # Added for scheduler
from Crypto.PublicKey import RSA

def generate_fake_rsa_key(original_key):
    """Generates a new fake RSA key based on an original key template."""
    try:
        rsa_key = RSA.generate(2048)
        new_kid = ''.join(random.choices(string.hexdigits, k=40)).lower()
        
        exponent_int = 65537
        exponent_b64 = base64.urlsafe_b64encode(exponent_int.to_bytes((exponent_int.bit_length() + 7) // 8, 'big')).rstrip(b'=').decode('utf-8')

        new_key = {
            "kty": "RSA",
            "e": exponent_b64,
            "use": original_key.get("use", "sig"),
            "alg": original_key.get("alg", "RS256"),
            "kid": new_kid,
            "n": base64.urlsafe_b64encode(rsa_key.n.to_bytes(256, 'big')).rstrip(b'=').decode('utf-8'),
        }
        return new_key
    except Exception as e:
        print(f"ERROR: Failed to generate new RSA key: {e}")
        return None

def select_key_to_replace(keys_data):
    """Randomly selects one of the keys to be replaced."""
    # This function assumes keys_data is valid and keys_data["keys"] is not empty.
    # Validation is expected to be done by the caller (rotate_key).
    num_keys = len(keys_data["keys"])
    return random.randint(0, num_keys - 1)

def rotate_key():
    """Orchestrates the key rotation process."""
    print("INFO: Attempting key rotation...")
    keys_data = None
    try:
        with open("keys.json", 'r') as f:
            keys_data = json.load(f)
    except FileNotFoundError:
        print("ERROR: keys.json not found. Skipping rotation cycle.")
        return
    except json.JSONDecodeError as e:
        print(f"ERROR: keys.json is not a valid JSON file: {e}. Skipping rotation cycle.")
        return
    except Exception as e:
        print(f"ERROR: An unexpected error occurred while reading keys.json: {e}. Skipping rotation cycle.")
        return

    if not isinstance(keys_data, dict) or "keys" not in keys_data or not isinstance(keys_data["keys"], list):
        print("ERROR: keys.json does not have the expected structure: {'keys': [...]}. Skipping rotation cycle.")
        return
    
    if not keys_data["keys"]:
        # This means the "keys" list is empty.
        # The problem states "at least two keys" - this check handles 0 keys.
        # If one key is present, it will be used as a template.
        # If the requirement is strictly "at least two keys" for rotation to even be considered,
        # this condition should be `len(keys_data["keys"]) < 2`.
        # For now, allowing a single key to be rotated (replaced by a new one using itself as template).
        print("ERROR: 'keys' array in keys.json is empty. Cannot select a key to use as a template. Skipping rotation cycle.")
        return

    try:
        key_index_to_replace = select_key_to_replace(keys_data)
    except ValueError as e: # Should not happen if the above checks are done correctly
        print(f"ERROR: Could not select key to replace: {e}. Skipping rotation cycle.")
        return
        
    original_key = keys_data["keys"][key_index_to_replace]
    original_kid = original_key.get("kid", "N/A")
    
    new_fake_key = generate_fake_rsa_key(original_key)
    if new_fake_key is None:
        print("ERROR: Failed to generate new key. Skipping rotation cycle.")
        return
    
    print(f"INFO: Successfully generated new key. Old KID: {original_kid}, New KID: {new_fake_key['kid']}. Index: {key_index_to_replace}.")
    keys_data["keys"][key_index_to_replace] = new_fake_key
    
    try:
        with open("keys.json", 'w') as f:
            json.dump(keys_data, f, indent=4)
        print(f"INFO: Successfully rotated key (Old KID: {original_kid}, New KID: {new_fake_key['kid']}) and updated keys.json.")
    except IOError as e:
        print(f"ERROR: Could not write updated keys to keys.json (IOError): {e}. Rotation failed for this cycle.")
    except Exception as e:
        print(f"ERROR: An unexpected error occurred while writing keys.json: {e}. Rotation failed for this cycle.")

if __name__ == "__main__":
    print("INFO: Key rotation scheduler starting...")
    # Schedule the job
    schedule.every(15).minutes.do(rotate_key)
    # For easier testing of the rotation logic itself, one might reduce the schedule:
    # schedule.every(10).seconds.do(rotate_key)

    # Perform an initial rotation immediately if desired.
    # print("INFO: Performing initial key rotation.")
    # rotate_key() 
    
    print("INFO: Key rotation scheduler started. Waiting for scheduled rotations. Press Ctrl+C to exit.")
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        print("INFO: Scheduler stopped by user.")
    except Exception as e:
        print(f"ERROR: An unexpected error occurred in the scheduler loop: {e}")
    finally:
        print("INFO: Exiting key rotator script.")
