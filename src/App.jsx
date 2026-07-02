import "./styles/App.css";
import MapView from "./components/MapView";
import RainLegend from "./components/RainLegend";
import { useEffect, useState } from "react";
import { fetchRainSynop } from "./services/panahonApi"
import { parseRainStations } from "./utils/rainParser";

function App() {

  const [stations, setStations] = useState([]);
  const [footprints, setFootprints] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    /* Loading, Error, and Empty States */
    async function fetchStations() {
      setLoading(true);
      setError(null);

      try {
        /* Load rainfall stations */
        const response = await fetchRainSynop();

        const parsedStations = parseRainStations(response);

        console.table(parsedStations);

        setStations(parsedStations);

        /* Load rainfall stations */
        const footprintResponse = await fetch("/data/s1a_footprints.geojson");

        if (!footprintResponse.ok) {
          throw new Error("Failed to load S1A footprint polygons.");
        }

        const footprintData = await footprintResponse.json();

        console.log("S1A Footprints:", footprintData);

        setFootprints(footprintData);
      } catch (err) {
        console.error(err);
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
        {loading && (
          <div className="status-message">
            Loading rainfall stations...
          </div>
        )}

        {!loading && error && (
          <div className="status-message error">
            {error}
          </div>
        )}

        {!loading && !error && stations.length === 0 && (
          <div className="status-message">
            No rainfall stations available.
          </div>
        )}

        {!loading && !error && stations.length > 0 && (
          <>
            <MapView 
              stations={stations}
              footprints={footprints} 
            />
            <RainLegend />
          </>
        )}
      </main>
    </div>
  );
}

export default App;