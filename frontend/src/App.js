import logo from './logo.svg';
import './App.css';
import {useState, useEffect} from 'react';
import Tracker from './tracker.js';

function App() {
  const [data, setData] = useState(null);
  const tracker = new Tracker("georgiClientId");

  useEffect(() => {
    fetch('http://localhost:8000/api/v1/test/')
      .then(res => res.json())
      .then(data => setData(data.data));
    
    tracker.verbose = true;
    tracker.identify("georgiUserId");
    tracker.startTracking();
  })

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <h1>An Awesome Blog </h1>
        <h3>On Django, React, Postgres, and Docker </h3>

        <p>{data}</p>
        <button onClick={() => tracker.track("click", [{buttonId: "1"}])}>Click me</button>
      </header>
    </div>
  ); 
}

export default App;
