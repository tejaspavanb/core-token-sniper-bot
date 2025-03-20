import React from 'react';
import axios from 'axios';

function TokenDetails({ match }) {
  const [token, setToken] = React.useState(null);

  React.useEffect(() => {
    const fetchToken = async () => {
      try {
        const response = await axios.get(`http://localhost:5000/api/tokens/${match.params.address}`);
        setToken(response.data);
      } catch (error) {
        console.error('Error fetching token details:', error);
      }
    };

    fetchToken();
  }, [match.params.address]);

  if (!token) {
    return <div>Loading token details...</div>;
  }

  return (
    <div className="token-details">
      <h2>Token Details</h2>
      <p>Address: {token.address}</p>
      <p>Launch Time: {new Date(token.launchTime * 1000).toLocaleString()}</p>
      <p>Total Supply: {token.totalSupply}</p>
      <p>Liquidity: {token.liquidity}</p>
      <p>Holder Count: {token.holderCount}</p>
    </div>
  );
}

export default TokenDetails;