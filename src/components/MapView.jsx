import { useEffect, useRef } from "react";
import { createRoot } from "react-dom/client";
import RainStationPopup from "./RainStationPopup";
import maplibregl from "maplibre-gl";
import "maplibre-gl/dist/maplibre-gl.css";

function MapView({ stations }) {
  /* Map general settings */
  const mapContainer = useRef(null);
  const map = useRef(null);

  // Initialize the map only once
  useEffect(() => {
    if (map.current) return;

    map.current = new maplibregl.Map({
      container: mapContainer.current,
      style: "https://demotiles.maplibre.org/style.json",
      center: [121.774, 12.8797],
      zoom: 5,
    });

    map.current.addControl(
      new maplibregl.NavigationControl(),
      "top-right"
    );
  }, []);

  /* Rendered rainfall stations*/
  // Update rainfall layer whenever stations change
  useEffect(() => {
    if (!map.current) return;

    const geojson = {
      type: "FeatureCollection",
      features: stations.map((station) => ({
        type: "Feature",
        properties: {
          id: station.id,
          stationName: station.stationName,
          rainfallMm: station.rainfallMm,
          observedAt: station.observedAt,
          latitude: station.latitude,
          longitude: station.longitude
        },
        geometry: {
          type: "Point",
          coordinates: [station.longitude, station.latitude],
        },
      })),
    };

    const updateRainfallLayer = () => {
      // Update existing source
      if (map.current.getSource("rainfall")) {
        map.current.getSource("rainfall").setData(geojson);
        return;
      }

      // Add source
      map.current.addSource("rainfall", {
        type: "geojson",
        data: geojson,
      });

      // Add layer
      map.current.addLayer({
        id: "rainfall-layer",
        type: "circle",
        source: "rainfall",

        paint: {
          "circle-radius": [
            "step",
            ["get", "rainfallMm"],
            5,
            1, 7,
            10, 9,
            25, 11,
            50, 13,
          ],

          "circle-color": [
            "step",
            ["get", "rainfallMm"],
            "#d6eaf8", // 0 mm
            1, "#aed6f1", // 1–10
            10, "#5dade2", // 10–25
            25, "#2874a6", // 25–50
            50, "#154360", // >50
          ],

          "circle-stroke-color": "#ffffff",
          "circle-stroke-width": 1,
        },
      });

      // Add pop-up
      map.current.on("click", "rainfall-layer", (e) => {
        const feature = e.features[0];
        const popupNode = document.createElement("div");
        const root = createRoot(popupNode);

        root.render(
          <RainStationPopup
            station={feature.properties}
          />
        );

        new maplibregl.Popup({
          closeButton: true,
          closeOnClick: true
        })
          .setLngLat(feature.geometry.coordinates)
          .setDOMContent(popupNode)
          .addTo(map.current);

      });

      map.current.on("mouseenter", "rainfall-layer", () => {
        map.current.getCanvas().style.cursor = "pointer";
      });

      map.current.on("mouseleave", "rainfall-layer", () => {
        map.current.getCanvas().style.cursor = "";
      });
    };

    // Wait until the style has loaded
    if (!map.current.isStyleLoaded()) {
      map.current.once("load", updateRainfallLayer);
    } else {
      updateRainfallLayer();
    }
  }, [stations]);

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