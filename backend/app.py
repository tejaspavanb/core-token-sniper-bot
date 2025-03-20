from flask import Flask, jsonify, request
from web3 import Web3
import joblib

app = Flask(__name__)
w3 = Web3(Web3.HTTPProvider('https://rpc.test2.btcs.network'))

# Load the trained model
model = joblib.load('token_predictor.pkl')

# Smart contract setup
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
contract_address = '0x7ed2467FBF8A04f11f149AF70f21E91D6C89dD12' # Address of deployed TokenTracker contract
token_tracker = w3.eth.contract(address=contract_address, abi=contract_abi)

@app.route('/test-connection')
def test_connection():
    if w3.is_connected():
        return "Connected to Core node successfully"
    else:
        return "Failed to connect to Core node", 500
    

@app.route('/test-contract')
def test_contract():
    try:
        # Call a simple function from your smart contract
        registered_tokens = token_tracker.functions.getRegisteredTokens().call()
        return jsonify({
            'message': 'Successfully called smart contract',
            'registeredTokens': registered_tokens
        })
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500
    
@app.route('/api/tokens', methods=['GET'])
def get_tokens():
    tokens = token_tracker.functions.getRegisteredTokens().call()
    token_list = []
    for token_address in tokens:
        token_info = token_tracker.functions.getTokenInfo(token_address).call()
        token_list.append({
            'address': token_address,
            'launchTime': token_info[1],
            'totalSupply': token_info[2],
            'liquidity': token_info[3],
            'holderCount': token_info[4]
        })
    return jsonify(token_list)

@app.route('/api/tokens/<address>', methods=['GET'])
def get_token(address):
    token_info = token_tracker.functions.getTokenInfo(address).call()
    return jsonify({
        'address': address,
        'launchTime': token_info[1],
        'totalSupply': token_info[2],
        'liquidity': token_info[3],
        'holderCount': token_info[4]
    })

@app.route('/api/tokens/metrics', methods=['GET'])
def get_metrics():
    # Implement filtering logic
    return jsonify({
        'minLiquidity': 0,
        'maxLiquidity': 1000000,
        'minHolderCount': 0,
        'maxHolderCount': 10000
    })

@app.route('/api/predict', methods=['POST'])
def predict():
    data = request.json
    prediction = model.predict([[
        data['liquidity'],
        data['holderCount'],
        data['totalSupply'],
        data['launchTime']
    ]])
    return jsonify({'prediction': int(prediction[0])})

if __name__ == '__main__':
    app.run(debug=True)