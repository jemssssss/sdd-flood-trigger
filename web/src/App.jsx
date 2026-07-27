import "./styles/App.css";
import MapView from "./components/MapView";
import LayerControl from "./components/LayerControl";
import RainLegend from "./components/RainLegend";
import FloodSummary from "./components/FloodSummary";
import { useEffect, useState } from "react";

const BACKEND_URL = import.meta.env.VITE_BACKEND_BASE_URL;

function App() {

  const [synopticStations, setSynopticStations] = useState([]);
  const [awsStations, setAwsStations] = useState([]);

  const [footprints, setFootprints] = useState(null);
  const [panahonSummary, setPanahonSummary] = useState({ moderate: [], heavy: [], });
  const [ecmwfSummary, setEcmwfSummary] = useState({ moderate: [], heavy: [], });
  const [passInfo, setPassInfo] = useState(null);

  const [showSynoptic, setShowSynoptic] = useState(true);
  const [showAWS, setShowAWS] = useState(true);
  const [showPanahonFootprints, setShowPanahonFootprints] = useState(true);
  const [showEcmwfFootprints, setShowEcmwfFootprints] = useState(false);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

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

        const [panahonResponse, ecmwfResponse] =
        await Promise.all([
          fetch(`${BACKEND_URL}/panahon/footprints`),
          fetch(`${BACKEND_URL}/ecmwf/footprints`)
        ]);

        if (!synopticResponse.ok || !awsResponse.ok) {
          throw new Error("Backend request for rainfall stations failed.");
        }

        if (!panahonResponse.ok) {
          throw new Error("Failed to compute footprints (Panahon data).");
        }

        if (!ecmwfResponse.ok) {
          throw new Error("Failed to compute footprints (ECMWF data).");
        }

        const synopticStations = await synopticResponse.json();
        const awsStations = await awsResponse.json();
        const panahonData = await panahonResponse.json();
        const ecmwfData = await ecmwfResponse.json();

        console.table(synopticStations);
        console.table(awsStations);
        console.log("Panahon API Data");
        console.table(
          panahonData.geojson.features.map(feature => ({
            tile: feature.properties.TileNumber,
            rainfall: feature.properties.averageRainfall
          }))
        );
        console.log("ECMWF API Data");
        console.table(
          ecmwfData.geojson.features.map(feature => ({
            tile: feature.properties.TileNumber,
            rainfall: feature.properties.ecmwfRainfall
          }))
        );

        setSynopticStations(synopticStations);
        setAwsStations(awsStations);
        
        const merged = structuredClone(panahonData.geojson);
        merged.features.forEach((feature) => {
          const tile = feature.properties.TileNumber;
          const ecmwfFeature =
            ecmwfData.geojson.features.find(f => f.properties.TileNumber === tile);

          feature.properties.ecmwfRainfall = ecmwfFeature?.properties.ecmwfRainfall ?? null;
        });
        setFootprints(merged);

        setPanahonSummary(panahonData.summary);
        setEcmwfSummary(ecmwfData.summary);
        setPassInfo(panahonData.passInfo);

      }

      catch (err) {
        console.error(err);
        setError(err.message);
      }

      finally {
        setLoading(false);
      }

    } fetchStations();
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

              showPanahonFootprints={showPanahonFootprints}
              setShowPanahonFootprints={setShowPanahonFootprints}

              showEcmwfFootprints={showEcmwfFootprints}
              setShowEcmwfFootprints={setShowEcmwfFootprints}

            />

            <FloodSummary

              panahonSummary={panahonSummary}
              ecmwfSummary={ecmwfSummary}
              
            />

            {passInfo && (
              <div className="satellite-pass-status">
                {passInfo.hasPass ? (
                  <>
                    <strong>{passInfo.satellite} pass: Strip {passInfo.strip}</strong>
                    <span>Only Strip {passInfo.strip} footprint tiles are shown.</span>
                  </>
                ) : (
                  <>
                    <strong>No Satellite Pass</strong>
                    <span>
                      {passInfo.satellite} has no Philippines pass on {passInfo.passDate}.
                    </span>
                  </>
                )}
              </div>
            )}

            <MapView

              synopticStations={synopticStations}
              awsStations={awsStations}
              footprints={footprints}

              showSynoptic={showSynoptic}
              showAWS={showAWS}
              showPanahonFootprints={showPanahonFootprints}
              showEcmwfFootprints={showEcmwfFootprints}

            />

            <RainLegend/>

          </>
        )}
      </main>
    </div>
  );
}

export default App;
