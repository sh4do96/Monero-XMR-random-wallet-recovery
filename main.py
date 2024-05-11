import time

from monero.wallet import Wallet
from monero.backends.jsonrpc import JSONRPCWallet
import os
import subprocess
import requests
import json
import random
import string

def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    print("Random string of length", length, "is:", result_str)


def generate_phrase_from_wordlist(wordlist_file, phrase_length):
    # Read the wordlist file
    with open("wordlist.txt", 'r') as file:
        words = [line.strip() for line in file]

    # Generate a random phrase of the specified length
    import random
    phrase = ' '.join(random.sample(words, phrase_length))

    return phrase


def restore_wallet(recovery_seed, filename):
    url = "http://127.0.0.1:28088/json_rpc"
    payload = {
        "jsonrpc": "2.0",
        "id": 0,
        "method": "restore_deterministic_wallet",
        "params": {
            "restore_height": 0,
            "filename": filename,
            "password": "",
            "seed": recovery_seed,
            "language": "english"
        }
    }
    payload_balance = {
        "jsonrpc":"2.0",
        "id":"0",
        "method":"get_balance",
        "params":
            {
                "account_index":0,
                "address_indices":[0,1]
            }
    }
    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url, data=json.dumps(payload), headers=headers)
    response2 = requests.post(url, data=json.dumps(payload_balance), headers=headers)
    if response.status_code == 200:
        result = response.json()
        result2 = response2.json()
        print(result)
        print(result2)
        if result2["result"]["balance"] == 0:
            print("NotFound!")
        else:
            print("Found!")
            time.sleep(9999)
        if 'error' in result:
            print(f"Błąd przy przywracaniu portfela: {result['error']['message']}")
            return False
        else:
            return True
    else:
        print(f"Błąd HTTP: {response.status_code}")
        return False

if __name__ == "__main__":
    wordlist_file = 'monero_wordlist.txt'
    phrase_length = 24

    # Generate a phrase from the wordlist



    # Set the wallet name
    wallet_name = 'my_new_wallet'

    # Restore the Monero wallet
    while True:
        phrase = generate_phrase_from_wordlist(wordlist_file, phrase_length)
        print('Generated phrase:', phrase)
        # time.sleep(0.01)
        
        restore_wallet(phrase, get_random_string(8))
