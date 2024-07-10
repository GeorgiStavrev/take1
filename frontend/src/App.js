import logo from './logo.svg';
import './App.css';
import {useState, useEffect} from 'react';

function App() {
  const [data, setData] = useState(null);

  useEffect(() => {    
    if (window.tracker !== undefined && window.tracker !== null) {
      window.tracker.identify("georgiUserId");
    }
  })

  const handleClick = (clickEvent) => {
    const id = clickEvent.target.id;
    const tag = clickEvent.target.tagName;
    if (id !== null && id !== undefined && window.tracker !== undefined && window.tracker !== null) {
      var properties = [];
      properties.push({'type': tag});
      properties.push({'id': id});
      window.tracker.track("click", properties)
    }
  }

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <h1>An Awesome Blog </h1>
        <h3>On Django, React, Postgres, and Docker </h3>
        <p>{data}</p>
        <button onClick={handleClick} id="clickMe">Click me</button>
      </header>
    </div>
  ); 
}

export default App;
