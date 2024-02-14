import React, { useState, useEffect } from 'react';

function App() {
  // State to store the fetched data
  const [data, setData] = useState(null);

  // Function to fetch data from the API
  const fetchData = async () => {
    try {
      const response = await fetch('https://mcsbt-integration.ew.r.appspot.com/continue-watching');
      const jsonData = await response.json();
      setData(jsonData);
    } catch (error) {
      console.error("Error fetching data: ", error);
      setData(null);
    }
  };

  // useEffect to run once on component mount
  useEffect(() => {
    fetchData();
  }, []); // The empty array causes this effect to only run on mount

  // Render the fetched data
  return (
    <div className="App">
      <h1>Fetched Data1</h1>
      {data ? (
        <div>
          <p>{data}</p>
        </div>
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
}

export default App;
