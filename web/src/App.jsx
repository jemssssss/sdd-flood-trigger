import "./styles/App.css";
import MapView from "./components/MapView";
import LayerControl from "./components/LayerControl";
import RainLegend from "./components/RainLegend";
import FloodSummary from "./components/FloodSummary";
import { useEffect, useState } from "react";
import { getAccumulationTimes } from "./utils/timeUtils";

const BACKEND_URL = import.meta.env.VITE_BACKEND_BASE_URL;

function App() {

  const [synopticStations, setSynopticStations] = useState([]);
  const [awsStations, setAwsStations] = useState([]);
  const [footprints, setFootprints] = useState(null);
  const [floodSummary, setFloodSummary] = useState({moderate: [], heavy: []});
  const [showSynoptic, setShowSynoptic] = useState(true);
  const [showAWS, setShowAWS] = useState(true);
  const [showFootprints, setShowFootprints] = useState(true);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const { forecastTime, initTime, hour } = getAccumulationTimes();
  console.log("Accumulation hour:", hour);
  console.log("Forecast time:", forecastTime);
  console.log("Init time:", initTime);

  useEffect(() => {

    /* Loading, Error, and Empty States */

    async function fetchStations() {

    setLoading(true);
    setError(null);

    try {

      /* Fetching Rainfall Data */

      const [
        synopticResponse,
        awsResponse,
      ] = await Promise.all([

        fetch(`${BACKEND_URL}/panahon/synoptic`),
        fetch(`${BACKEND_URL}/panahon/aws`),

      ]);

      const footprintResponse = await fetch(
        `${import.meta.env.VITE_BACKEND_BASE_URL}/panahon/footprints` +
        `?t=${encodeURIComponent(forecastTime)}` +
        `&init=${encodeURIComponent(initTime)}`
      );

      if (
        !synopticResponse.ok ||
        !awsResponse.ok 
      ) {
        throw new Error("Backend request for rainfall stations failed.");
      }

      if (!footprintResponse.ok) {
        throw new Error("Failed to compute footprints.");
      }

      const synopticStations = await synopticResponse.json();
      const awsStations = await awsResponse.json();
      const footprintResult = await footprintResponse.json();

      console.table(synopticStations);
      console.table(awsStations);
      console.table(
        footprintResult.geojson.features.map(feature => ({
          tile: feature.properties.TileNumber,
          rainfall: feature.properties.averageRainfall
        }))
      );

      setSynopticStations(synopticStations);
      setAwsStations(awsStations);
      setFootprints(footprintResult.geojson);
      setFloodSummary(footprintResult.summary);

    }

    catch (err) {
      console.error(err);
      setError(err.message);
    }

    finally {
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
            Loading rainfall data...
          </div>
        )}

        {!loading && error && (
          <div className="status-message error">
            {error}
          </div>
        )}

        {!loading && !error && synopticStations.length === 0 && awsStations.length === 0 && (
          <div className="status-message">
            No rainfall stations available.
          </div>
        )}

        {!loading && !error && synopticStations.length > 0 && awsStations.length > 0 && (
          <>

            <LayerControl

              showSynoptic={showSynoptic}
              setShowSynoptic={setShowSynoptic}

              showAWS={showAWS}
              setShowAWS={setShowAWS}

              showFootprints={showFootprints}
              setShowFootprints={setShowFootprints}

            />

            <FloodSummary

              summary={floodSummary}

            />

            <MapView

              synopticStations={synopticStations}
              awsStations={awsStations}

              showSynoptic={showSynoptic}
              showAWS={showAWS}
              showFootprints={showFootprints}

              footprints={footprints}

            />

            <RainLegend/>

          </>
        )}
      </main>
    </div>
  );
}

export default App;