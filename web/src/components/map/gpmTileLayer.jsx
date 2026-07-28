import { createRoot } from "react-dom/client";
import bbox from "@turf/bbox";
import FootprintPopup from "../FootprintPopup";

export function updateGPMLayer({
  map,
  sourceId,
  fillLayerId,
  outlineLayerId,
  footprints,
  visible,
  hasFitBounds,
  stationPopup,
  footprintPopup,
}) {

  if (!footprints) return;

  /* Source */

  if (map.getSource(sourceId)) {
    map.getSource(sourceId).setData(footprints);
  } else {
    map.addSource(sourceId, {
      type: "geojson",
      data: footprints,
    });

    /* Fill layer */

    map.addLayer({
      id: fillLayerId,
      type: "fill",
      source: sourceId,
      paint: {
        "fill-color": [
          "step",
          ["coalesce", ["get", "gpmRainfall"], 0],
          "#eef7ff",
          1, "#00e100",
          60, "#ffaa00",
          180, "#ff0000",
        ],
        "fill-opacity": 0.30,
      },
    });

    /* Outline layer */

    map.addLayer({
      id: outlineLayerId,
      type: "line",
      source: sourceId,
      paint: {
        "line-color": "#1f78b4",
        "line-width": 2,
      },
    });

    /* Keep stations on top */

    if (map.getLayer("synoptic-layer")) {
      map.moveLayer("synoptic-layer");
    }

    if (map.getLayer("aws-layer")) {
      map.moveLayer("aws-layer");
    }

    /* Popup */

    map.on("click", fillLayerId, (e) => {
      const stations = map.queryRenderedFeatures(e.point, {
        layers: [
          "synoptic-layer",
          "aws-layer",
        ],
      });

      if (stations.length > 0) return;

      const feature = e.features[0];
      const popupNode = document.createElement("div");
      const root = createRoot(popupNode);

      root.render(
        <FootprintPopup
          footprint={feature.properties}
        />
      );

      stationPopup.current.remove();
      footprintPopup.current
        .setLngLat(e.lngLat)
        .setDOMContent(popupNode)
        .addTo(map);

    });

    /* Cursor */

    map.on("mouseenter", fillLayerId, () => {
      map.getCanvas().style.cursor = "pointer";
    });

    map.on("mouseleave", fillLayerId, () => {
      map.getCanvas().style.cursor = "";
    });

  }

  /* Update style */

  map.setPaintProperty(
    fillLayerId,
    "fill-color",
    [
      "step",
      ["coalesce", ["get", "gpmRainfall"], 0],
      "#eef7ff",
      1, "#00e100",
      60, "#ffaa00",
      180, "#ff0000",
    ]
  );

  /* Visibility */

  map.setLayoutProperty(
    fillLayerId,
    "visibility",
    visible
      ? "visible"
      : "none"
  );

  map.setLayoutProperty(
    outlineLayerId,
    "visibility",
    visible
      ? "visible"
      : "none"
  );

  /* Zoom once */

  if (!hasFitBounds.current) {
    const bounds = bbox(footprints);
    map.fitBounds(
      bounds,
      {
        padding: 40,
        duration: 1000,
      }
    );

    hasFitBounds.current = true;

  }

}