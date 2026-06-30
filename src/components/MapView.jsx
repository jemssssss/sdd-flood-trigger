import { useEffect, useRef, useState } from "react";
import maplibregl from "maplibre-gl";
import "maplibre-gl/dist/maplibre-gl.css";
import { fetchRainSynop } from "../services/panahonApi";

function MapView() {
  const mapContainer = useRef(null);
  const map = useRef(null);

  useEffect(() => {
		/* Map Settings */
    if (map.current) return;

    map.current = new maplibregl.Map({
      container: mapContainer.current,
      style: "https://demotiles.maplibre.org/style.json",
      center: [121.774, 12.8797], // centered at the Philippines
      zoom: 5,
    });

    map.current.addControl(new maplibregl.NavigationControl(), "top-right"); // Map navigation control buttons
  }, []);

  return (
    <div
      ref={mapContainer}
      style={{
        width: "100%",
        height: "100%",
      }}
    />
  );
}

export default MapView;