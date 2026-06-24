// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

// Blocklist: stores blocked attacker IPs permanently and immutably on-chain.
contract Blocklist {
    string[] private blockedIPs;
    mapping(string => bool) private blocked;

    event IPBlocked(string ip, uint256 timestamp);

    // Add an attacker IP to the on-chain blocklist (only if not already present).
    function blockIP(string memory ip) public {
        if (!blocked[ip]) {
            blocked[ip] = true;
            blockedIPs.push(ip);
            emit IPBlocked(ip, block.timestamp);
        }
    }

    // Check whether a given IP is blocked.
    function isBlocked(string memory ip) public view returns (bool) {
        return blocked[ip];
    }

    // Return the full list of blocked IPs.
    function getBlockedIPs() public view returns (string[] memory) {
        return blockedIPs;
    }
}
