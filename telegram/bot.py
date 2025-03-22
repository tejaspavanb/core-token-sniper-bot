import telebot
import requests
import threading
import time
from web3 import Web3
from web3.middleware import ExtraDataToPOAMiddleware
from datetime import datetime  # Add this import
from eth_account import Account 

# Initialize Telegram bot
bot = telebot.TeleBot('INSERT_THE_BOT_API')

# Connect to Core blockchain
w3 = Web3(Web3.HTTPProvider('https://rpc.test2.btcs.network'))
w3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)
# Smart contract ABI and address
contract_abi = [
    {
      "anonymous": False,
      "inputs": [
        {
          "indexed": True,
          "internalType": "address",
          "name": "tokenAddress",
          "type": "address"
        },
        {
          "indexed": False,
          "internalType": "uint256",
          "name": "launchTime",
          "type": "uint256"
        }
      ],
      "name": "TokenRegistered",
      "type": "event"
    },
    {
      "inputs": [],
      "name": "getRegisteredTokens",
      "outputs": [
        {
          "internalType": "address[]",
          "name": "",
          "type": "address[]"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "_tokenAddress",
          "type": "address"
        }
      ],
      "name": "getTokenInfo",
      "outputs": [
        {
          "components": [
            {
              "internalType": "address",
              "name": "tokenAddress",
              "type": "address"
            },
            {
              "internalType": "uint256",
              "name": "launchTime",
              "type": "uint256"
            },
            {
              "internalType": "uint256",
              "name": "totalSupply",
              "type": "uint256"
            },
            {
              "internalType": "uint256",
              "name": "liquidity",
              "type": "uint256"
            },
            {
              "internalType": "uint256",
              "name": "holderCount",
              "type": "uint256"
            }
          ],
          "internalType": "struct TokenTracker.TokenInfo",
          "name": "",
          "type": "tuple"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "_tokenAddress",
          "type": "address"
        }
      ],
      "name": "registerToken",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "name": "registeredTokens",
      "outputs": [
        {
          "internalType": "address",
          "name": "",
          "type": "address"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "",
          "type": "address"
        }
      ],
      "name": "tokenRegistry",
      "outputs": [
        {
          "internalType": "address",
          "name": "tokenAddress",
          "type": "address"
        },
        {
          "internalType": "uint256",
          "name": "launchTime",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "totalSupply",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "liquidity",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "holderCount",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "_tokenAddress",
          "type": "address"
        },
        {
          "internalType": "uint256",
          "name": "_holderCount",
          "type": "uint256"
        }
      ],
      "name": "updateHolderCount",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "_tokenAddress",
          "type": "address"
        },
        {
          "internalType": "uint256",
          "name": "_liquidity",
          "type": "uint256"
        }
      ],
      "name": "updateLiquidity",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    }
]  # ABI from deployed TokenTracker contract
contract_address = '0x7ed2467FBF8A04f11f149AF70f21E91D6C89dD12'  # Address of deployed TokenTracker contract
token_tracker = w3.eth.contract(address=contract_address, abi=contract_abi)

# Store active users and their transaction data
active_users = {}
pending_transactions = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    if chat_id not in active_users:
        active_users[chat_id] = {
            'address': None,
            'private_key': None
        }
        print(f"New user added: {chat_id}")
    bot.reply_to(message, "Welcome to Core Token Sniper! Use /help to see available commands.")

@bot.message_handler(commands=['help'])
def send_help(message):
    help_text = """
Available Commands:
/start - Start the bot
/help - Show this help message
/snipe - Activate token sniping mode
/tokens - List registered tokens
/tx <transaction_hash> - Get transaction details
/newwallet - Create a new wallet
/importwallet - Import a wallet with private key
/send <token_address> <recipient> <amount> - Send tokens
/cancel - Cancel pending transaction
/history - View transaction history
"""
    bot.reply_to(message, help_text)

@bot.message_handler(commands=['snipe'])
def start_sniping(message):
    chat_id = message.chat.id
    if chat_id not in active_users:
        active_users[chat_id] = {
            'address': None,
            'private_key': None
        }
    bot.reply_to(message, "Sniping mode activated! You'll be notified of new token launches.")

@bot.message_handler(commands=['tokens'])
def list_tokens(message):
    try:
        token_addresses = token_tracker.functions.getRegisteredTokens().call()
        if not token_addresses:
            bot.reply_to(message, "No tokens have been registered yet.")
            return
        
        response = "Registered tokens:\n"
        for i, addr in enumerate(token_addresses, 1):
            try:
                token_info = token_tracker.functions.getTokenInfo(addr).call()
                response += f"{i}. Address: {addr}\n   Launch Time: {token_info[1]}\n   Liquidity: {token_info[3]}\n\n"
            except Exception as e:
                response += f"{i}. Address: {addr} (Error fetching details)\n"
        
        bot.reply_to(message, response)
    except Exception as e:
        bot.reply_to(message, f"Error fetching tokens: {str(e)}")

@bot.message_handler(commands=['tx'])
def get_transaction_details(message):
    try:
        _, tx_hash = message.text.split(' ')
        tx = w3.eth.get_transaction(tx_hash)
        receipt = w3.eth.get_transaction_receipt(tx_hash)
        
        status = "Success" if receipt.status == 1 else "Failed"
        timestamp = w3.eth.get_block(tx.blockNumber).timestamp
        dt = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
        
        response = f"Transaction Details:\n"
        response += f"Hash: {tx_hash}\n"
        response += f"From: {tx['from']}\n"
        response += f"To: {tx['to']}\n"
        response += f"Value: {w3.from_wei(tx['value'], 'ether')} CORE\n"
        response += f"Gas Used: {receipt.gasUsed}\n"
        response += f"Status: {status}\n"
        response += f"Block: {tx.blockNumber}\n"
        response += f"Timestamp: {dt}\n"
        
        bot.reply_to(message, response)
    except Exception as e:
        bot.reply_to(message, f"Error fetching transaction details: {str(e)}")

@bot.message_handler(commands=['newwallet'])
def create_new_wallet(message):
  chat_id = message.chat.id

    # Ensure chat_id exists in active_users before accessing its keys
  if chat_id not in active_users:
    active_users[chat_id] = {}  # Initialize user entry

  account = Account.create()
  private_key = account._private_key.hex()  # Correct way to access the private key

  active_users[chat_id]['address'] = account.address
  active_users[chat_id]['private_key'] = private_key
  response = "🆕 **New Wallet Created:**\n"
  response += f"📍 Address: `{account.address}`\n"
  response += f"🔑 Private Key: `{private_key}`\n"
  response += "\n⚠️ **Keep your private key secure!** ⚠️\nDo not share it with anyone."

  bot.reply_to(message, response, parse_mode="Markdown")

@bot.message_handler(commands=['importwallet'])
def import_wallet(message):
    chat_id = message.chat.id
    parts = message.text.split(" ")

    # Ensure the user provided a private key
    if len(parts) < 2:
        bot.reply_to(message, "❌ Usage: `/importwallet <your_private_key>`\nExample: `/importwallet 0xabc123...`", parse_mode="Markdown")
        return

    private_key = parts[1].strip()

    # Validate private key format
    if not private_key.startswith("0x") or len(private_key) != 66:
        bot.reply_to(message, "❌ Invalid private key format. It should be a 64-character hex key starting with `0x`.", parse_mode="Markdown")
        return

    try:
        # Ensure chat_id exists in active_users before using it
        if chat_id not in active_users:
            active_users[chat_id] = {}

        account = Account.from_key(private_key)  # Import wallet using the private key
        active_users[chat_id]['address'] = account.address
        active_users[chat_id]['private_key'] = private_key

        response = "✅ **Wallet Imported Successfully!**\n"
        response += f"📍 Address: `{account.address}`\n"
        response += "\n⚠️ **Keep your private key secure!** ⚠️\nDo not share it with anyone."

        bot.reply_to(message, response, parse_mode="Markdown")

    except Exception as e:
        bot.reply_to(message, f"❌ Error importing wallet: {str(e)}")



@bot.message_handler(commands=['send'])
def send_tokens(message):
    chat_id = message.chat.id
    user = active_users.get(chat_id)
    
    if not user or not user['address'] or not user['private_key']:
        bot.reply_to(message, "Please create or import a wallet first using /newwallet or /importwallet")
        return
    
    try:
        _, token_address, recipient, amount = message.text.split(' ')
        amount_wei = w3.to_wei(float(amount), 'ether')
        
        # Get token contract
        token_contract = w3.eth.contract(address=token_address, abi=[
            {
                "constant": False,
                "inputs": [
                    {"name": "_to", "type": "address"},
                    {"name": "_value", "type": "uint256"}
                ],
                "name": "transfer",
                "outputs": [{"name": "success", "type": "bool"}],
                "payable": False,
                "stateMutability": "nonpayable",
                "type": "function"
            }
        ])
        
        # Build transaction
        nonce = w3.eth.get_transaction_count(user['address'])
        gas_price = w3.eth.gas_price
        
        tx = token_contract.functions.transfer(recipient, amount_wei).build_transaction({
            'chainId': w3.eth.chain_id,
            'gas': 200000,
            'gasPrice': gas_price,
            'nonce': nonce,
        })
        
        # Sign transaction
        signed_tx = w3.eth.account.sign_transaction(tx, user['private_key'])
        
        # Send transaction
        tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        
        pending_transactions[chat_id] = {
            'hash': tx_hash.hex(),
            'to': recipient,
            'amount': amount,
            'token': token_address,
            'status': 'pending'
        }
        
        response = "Transaction initiated!\n"
        response += f"Hash: {tx_hash.hex()}\n"
        response += f"Check status with /status {tx_hash.hex()}\n"
        response += "Use /cancel to abort this transaction"
        
        bot.reply_to(message, response)
    except Exception as e:
        bot.reply_to(message, f"Error sending tokens: {str(e)}")     
@bot.message_handler(commands=['cancel'])
def cancel_transaction(message):
    chat_id = message.chat.id
    if chat_id not in pending_transactions:
        bot.reply_to(message, "No pending transactions to cancel.")
        return
    
    tx_data = pending_transactions.pop(chat_id)
    bot.reply_to(message, f"Transaction to {tx_data['to']} for {tx_data['amount']} {tx_data['token']} cancelled.")

@bot.message_handler(commands=['status'])
def check_transaction_status(message):
    try:
        _, tx_hash = message.text.split(' ')
        tx = w3.eth.get_transaction(tx_hash)
        receipt = w3.eth.get_transaction_receipt(tx_hash)
        
        status = "Success" if receipt.status == 1 else "Failed"
        response = f"Transaction Status:\n"
        response += f"Hash: {tx_hash}\n"
        response += f"Status: {status}\n"
        response += f"Block: {tx.blockNumber}\n"
        
        bot.reply_to(message, response)
    except Exception as e:
        bot.reply_to(message, f"Error checking transaction status: {str(e)}")

@bot.message_handler(commands=['history'])
def transaction_history(message):
    chat_id = message.chat.id
    user = active_users.get(chat_id)
    
    if not user or not user['address']:
        bot.reply_to(message, "Please create or import a wallet first using /newwallet or /importwallet")
        return
    
    try:
        # This would require implementing a more complex transaction history lookup
        # For simplicity, we'll just show pending transactions for now
        if chat_id in pending_transactions:
            tx_data = pending_transactions[chat_id]
            response = "Pending Transaction:\n"
            response += f"To: {tx_data['to']}\n"
            response += f"Amount: {tx_data['amount']}\n"
            response += f"Token: {tx_data['token']}\n"
            response += f"Status: {tx_data['status']}\n"
            response += f"Hash: {tx_data['hash']}\n"
        else:
            response = "No recent transaction history available."
        
        bot.reply_to(message, response)
    except Exception as e:
        bot.reply_to(message, f"Error retrieving transaction history: {str(e)}")

def check_for_events():
    print("Starting token monitoring...")
    # Get the latest block number
    latest_block = w3.eth.block_number
    print(f"Current block number: {latest_block}")
    
    # Initialize last checked block
    last_checked_block = latest_block
    
    while True:
        try:
            # Get current block number
            current_block = w3.eth.block_number
            
            if current_block > last_checked_block:
                print(f"Checking blocks {last_checked_block} to {current_block}")
                
                # Create a filter for the TokenRegistered event
                event_signature_hash = w3.keccak(text="TokenRegistered(address,uint256)").hex()
                # Add 0x prefix to the event signature hash
                event_signature_hash = f"0x{event_signature_hash}"
                
                # Get logs for the event
                logs = w3.eth.get_logs({
                    'fromBlock': last_checked_block,
                    'toBlock': current_block,
                    'address': contract_address,
                    'topics': [event_signature_hash]
                })
                
                for log in logs:
                    # Decode the event data
                    decoded_log = token_tracker.events.TokenRegistered().process_log(log)
                    token_address = decoded_log['args']['tokenAddress']
                    launch_time = decoded_log['args']['launchTime']
                    
                    print(f"New token detected: {token_address}")
                    
                    # Try to get token info
                    try:
                        token_info = token_tracker.functions.getTokenInfo(token_address).call()
                        
                        # Notify all active users
                        for user_id in active_users:
                            notification = (
                                f"🚀 New token detected!\n"
                                f"Address: {token_address}\n"
                                f"Launch Time: {launch_time}\n"
                                f"Total Supply: {token_info[2]}\n"
                                f"Liquidity: {token_info[3]}\n"
                                f"Holders: {token_info[4]}"
                            )
                            bot.send_message(user_id, notification)
                    except Exception as e:
                        print(f"Error getting token info: {str(e)}")
                
                # Update the last checked block
                last_checked_block = current_block
            
            # Sleep to avoid hammering the RPC
            time.sleep(10)
        except Exception as e:
            print(f"Error in event monitoring: {str(e)}")
            time.sleep(30)  # Wait longer on error
if __name__ == "__main__":
    event_thread = threading.Thread(target=check_for_events)
    event_thread.daemon = True
    event_thread.start()
    print("Starting bot...")
    bot.polling(none_stop=True)
