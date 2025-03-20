// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

interface IERC20 {
    function totalSupply() external view returns (uint256);
    function balanceOf(address account) external view returns (uint256);
}

contract TokenTracker {
    struct TokenInfo {
        address tokenAddress;
        uint256 launchTime;
        uint256 totalSupply;
        uint256 liquidity;
        uint256 holderCount;
    }
    
    mapping(address => TokenInfo) public tokenRegistry;
    address[] public registeredTokens;
    
    event TokenRegistered(address indexed tokenAddress, uint256 launchTime);
    
    function registerToken(address _tokenAddress) external {
        require(tokenRegistry[_tokenAddress].tokenAddress == address(0), "Token already registered");
        
        uint256 totalSupply = IERC20(_tokenAddress).totalSupply();
        tokenRegistry[_tokenAddress] = TokenInfo({
            tokenAddress: _tokenAddress,
            launchTime: block.timestamp,
            totalSupply: totalSupply,
            liquidity: 0,
            holderCount: 0
        });
        
        registeredTokens.push(_tokenAddress);
        emit TokenRegistered(_tokenAddress, block.timestamp);
    }
    
    function updateLiquidity(address _tokenAddress, uint256 _liquidity) external {
        require(tokenRegistry[_tokenAddress].tokenAddress != address(0), "Token not registered");
        tokenRegistry[_tokenAddress].liquidity = _liquidity;
    }
    
    function updateHolderCount(address _tokenAddress, uint256 _holderCount) external {
        require(tokenRegistry[_tokenAddress].tokenAddress != address(0), "Token not registered");
        tokenRegistry[_tokenAddress].holderCount = _holderCount;
    }
    
    function getRegisteredTokens() external view returns (address[] memory) {
        return registeredTokens;
    }
    
    function getTokenInfo(address _tokenAddress) external view returns (TokenInfo memory) {
        return tokenRegistry[_tokenAddress];
    }
}