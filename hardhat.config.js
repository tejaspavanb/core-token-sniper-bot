require("@nomicfoundation/hardhat-toolbox");
require('dotenv').config();

module.exports = {
  solidity: "0.8.0",
  networks: {
    core: {
      url: process.env.CORE_NODE_URL,
      accounts: [process.env.PRIVATE_KEY],
      chainId:1114
    }
  }
};