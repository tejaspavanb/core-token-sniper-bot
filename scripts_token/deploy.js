// scripts/deploy.js
const { ethers } = require("hardhat");

async function main() {
  // Compile the contract
  await hre.run('compile');

  // Get the contract factory
  const TokenTracker = await ethers.getContractFactory("TokenTracker");

  // Deploy the contract
  const tokenTracker = await TokenTracker.deploy();

  // Wait for deployment to finish
  //await tokenTracker.deployed();

  console.log("TokenTracker deployed to:", tokenTracker.target);
}

// Run the main function and catch any errors
main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });



