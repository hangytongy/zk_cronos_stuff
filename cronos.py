import requests
from datetime import datetime, timedelta
import time

api_key= ""
token = "0x18d40Bd95e34d1a4fcaf9027Db11F6988e5B860A"
tele_chatid = ""
tele_token = ""

def get_block_height(timestamp):
    # Define the API URL
    url = "https://explorer-api.zkevm.cronos.org/api/v1/block/getBlockByTime"

    # Define the parameters
    params = {
        "timestamp": timestamp,  # Replace with the desired timestamp
        "apikey": api_key        # Replace with your API key
    }
    
    # Make the GET request
    response = requests.get(url, params=params)

    # Check the response
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        print(data)  # Process the data as needed
        
        return data['result']['blockHeight']
    else:
        print(f"Error: {response.status_code}, {response.text}")
        post_message(f"Error: {response.status_code}, {response.text}")

def get_logs(blockheight):
    
    start_block = blockheight - 250

    # Define the API URL
    url = "https://explorer-api.zkevm.cronos.org/api/v1/log/getLogs"

    # Define the parameters
    params = {
        "contractAddress": token,  # Replace with the contract address
        "startBlock": start_block,           # Replace with the starting block number
        "endBlock": blockheight,               # Replace with the ending block number
        "apikey": api_key                    # Replace with your API key
    }

    # Make the GET request
    response = requests.get(url, params=params)

    # Check the response
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()        
        return data['result']
    else:
        print(f"Error: {response.status_code}, {response.text}")
        post_message(f"Error: {response.status_code}, {response.text}")


def post_message(message):
    
    url = f"https://api.telegram.org/bot{tele_token}/sendMessage"
    
    payload = {'chat_id' : tele_chatid, 'text' : message, 'parse_mode' : "HTML"}
    response = requests.post(url, json=payload)
    
    if response.status_code == 200:
        print("post sucessful")
    else:
        print(f"error in posting {response}")

def main():

    tx_hashes = []
    
    while True:
        
        send_to_tele = []

        now = datetime.now()
        timestamp = int(now.timestamp())
        blockheight = get_block_height(timestamp)

        data = get_logs(blockheight)

        if data:
            for query in data:
                tx = query['transactionHash']
                if tx not in tx_hashes:
                    tx_hashes.append(tx)
                    print(f"https://explorer.zkevm.cronos.org/tx/{tx}")
                    send_to_tele.append(f"https://explorer.zkevm.cronos.org/tx/{tx}")
                   
        print("----------------------") 
        if send_to_tele:
            formatted_message = "\n".join(send_to_tele)
            formatted_message = "NEW TX ALERT!! \n\n" + formatted_message
            post_message(formatted_message)
                    
        time.sleep(10)

main()