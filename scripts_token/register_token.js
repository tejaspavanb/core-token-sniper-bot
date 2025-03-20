// scripts/register_token.js
const { ethers } = require("hardhat");

async function main() {
  // Get the contract factory
  const TokenTracker = await ethers.getContractFactory("TokenTracker");
  
  // Get the deployed contract instance
  const tokenTracker = await TokenTracker.attach(process.env.CONTRACT_ADDRESS);
  
  // Address of the new token to register
  const newTokenAddress = "0xf0FC3629534acA1e72139EAa724ff897B9a52bf3";
  
  // Register the new token
  console.log(`Registering token at address: ${newTokenAddress}`);
  const tx = await tokenTracker.registerToken(newTokenAddress);
  await tx.wait();
  
  console.log("Token registered successfully");
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });