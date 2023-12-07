import requests
import ecdsa
import hashlib
import base58
import time 
def generate_ethereum_wallet():
    # Generate a private key
    private_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)

    # Derive the corresponding public key
    public_key = private_key.get_verifying_key()

    # Derive the Ethereum address from the public key
    address = get_ethereum_address(public_key.to_string())

    return private_key.to_string().hex(), address

def get_ethereum_address(public_key_bytes):
    # Calculate the SHA-3 (Keccak-256) hash of the public key
    keccak256_hash = hashlib.sha3_256(public_key_bytes).digest()

    # Take the last 20 bytes as the Ethereum address
    ethereum_address = '0x' + keccak256_hash[-20:].hex()

    return ethereum_address

def check_balance(api_key, address):
    base_url = "https://api.etherscan.io/api"
    endpoint = "balance"

    # Construct the API URL
    api_url = f"{base_url}?module=account&action={endpoint}&address={address}&tag=latest&apikey={api_key}"

    try:
        # Make the API request
        response = requests.get(api_url)
        data = response.json()

        if data['status'] == '1':
            balance_wei = int(data['result'])
            return balance_wei
        else:
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def main():
    etherscan_api_key = 'your-api-key'

    while True:
        private_key, ethereum_address = generate_ethereum_wallet()

        print(f"Private Key: {private_key}")
        print(f"Ethereum Address: {ethereum_address}")

        balance_wei = check_balance(etherscan_api_key, ethereum_address)

        if balance_wei is not None:
            balance_eth = balance_wei / 1e18  # Convert from Wei to Ether
            print(f"Balance for {ethereum_address}: {balance_eth} ETH")

            if balance_wei > 0:
                with open('found.txt', 'a') as file:
                    file.write(f"Address: {ethereum_address}, Balance: {balance_eth} ETH\n")
                    print("Recorded in found.txt")
        else:
            print("Failed to retrieve balance. Please check your API key and address.")

        # Introduce a delay of, for example, 60 seconds before the next iteration
        time.sleep(0.2)

if __name__ == "__main__":
    main()