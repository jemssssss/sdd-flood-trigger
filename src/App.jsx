import "./styles/App.css";
import MapView from "./components/MapView";
import { useEffect, useState } from "react";
import { fetchRainSynop } from "./services/panahonApi"
import { parseRainStations } from "./utils/rainParser";

function App() {

  const [stations, setStations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    /* Loading, Error, and Empty States */
    async function fetchStations() {
      setLoading(true);
      setError(null);

      try {
        const response = await fetchRainSynop();

        console.log("Raw response:", response);

        const parsedStations = parseRainStations(response);

        console.table(parsedStations);

        setStations(parsedStations);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }

    fetchStations();
  }, []);

  return (
    <div className="app">
      <header className="header">
        <h1>SDD Flood Trigger Prototype</h1>
        <p>
          PAGASA/Panahon Rainfall Visualization
        </p>
      </header>

      <main className="content">
        <MapView />
      </main>
    </div>
  );
}

export default App;