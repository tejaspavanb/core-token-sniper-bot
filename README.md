# Core Token Sniper Bot

## Description
The **Core Token Sniper Bot** is a Telegram bot designed to monitor and notify users about new token launches on the Core blockchain. It provides real-time alerts for new token registrations and allows users to track token details including launch time, liquidity, and holder count.

## Features
- Real-time notifications for new token launches
- Detailed token information display
- Transaction history tracking
- Wallet creation and management
- Token sending capabilities
- Transaction status checking

## Installation

### Clone the repository:
```bash
git clone https://github.com/yourusername/core-token-sniper-bot.git
cd core-token-sniper-bot
```

### Install the required dependencies:
```bash
pip install telebot web3 eth_account requests
```

### Set up your Telegram bot:
1. Create a new bot via [@BotFather](https://t.me/BotFather) on Telegram.
2. Obtain your API token.
3. Replace the placeholder in the code with your actual API token.

### Configure your blockchain connection:
- Update the RPC provider URL in the code with your preferred Core blockchain RPC endpoint.

## Usage

### Start the bot:
```bash
python bot.py
```

### Interacting with the bot:
Search for your bot in Telegram and use the following commands:

#### Basic Commands
- `/start` - Initialize the bot
- `/help` - View available commands

#### Token Monitoring & Transactions
- `/snipe` - Activate token monitoring
- `/tokens` - List registered tokens
- `/tx <transaction_hash>` - Get transaction details
- `/status <transaction_hash>` - Check transaction status
- `/history` - View transaction history

#### Wallet Management
- `/newwallet` - Create a new wallet
- `/importwallet` - Import an existing wallet
- `/send <token_address> <recipient> <amount>` - Send tokens
- `/cancel` - Cancel a pending transaction

## Error Handling
The bot includes comprehensive error handling for:
- Network connectivity issues
- Invalid transaction hashes
- Wallet import errors
- Insufficient funds
- Invalid commands

## Contributing
Contributions are welcome! To contribute:
1. Fork the repository
2. Create a new branch (`git checkout -b feature-branch`)
3. Commit your changes (`git commit -m 'Add new feature'`)
4. Push to the branch (`git push origin feature-branch`)
5. Open a pull request

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contact
For any issues or suggestions, feel free to open an issue on GitHub or contact the developer at [your email or Telegram handle].

