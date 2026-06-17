// Deploys the Blocklist contract to the local Hardhat blockchain.
const hre = require("hardhat");

async function main() {
  const Blocklist = await hre.ethers.getContractFactory("Blocklist");
  const blocklist = await Blocklist.deploy();
  await blocklist.waitForDeployment();
  const addr = await blocklist.getAddress();
  console.log("=============================================");
  console.log("Blocklist deployed to:", addr);
  console.log("Copy this address into contract_address.py");
  console.log("=============================================");
}

main().catch((e) => { console.error(e); process.exitCode = 1; });
