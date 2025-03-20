import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import TokenList from './components/TokenList';
import TokenDetails from './components/TokenDetails';

function App() {
  return (
    <Router>
      <div className="App">
        <header className="App-header">
          <h1>Core Token Tracker</h1>
        </header>
        <main>
          <Routes>
            <Route path="/tokens/:address" element={<TokenDetails />} />
            <Route path="/" element={<TokenList />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;