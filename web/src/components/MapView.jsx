import { useEffect, useRef } from "react";
import { createRoot } from "react-dom/client";
import StationPopup from "./StationPopup";
import FootprintPopup from "./FootprintPopup";
import { updateStationLayer } from "./map/stationLayer";
import { updatePanahonLayer } from "./map/panahonTileLayer";
import { updateECMWFLayer } from "./map/ecmwfTileLayer";
import { updateGPMLayer } from "./map/gpmTileLayer";
import maplibregl from "maplibre-gl";
import bbox from "@turf/bbox";
import "maplibre-gl/dist/maplibre-gl.css";

function MapView({ 
  synopticStations, 
  awsStations, 
  showSynoptic, 
  showAWS, 
  footprints, 
  showPanahonFootprints, 
  showEcmwfFootprints,
  showGpmFootprints 
}) {
  /* Map general settings */
  const mapContainer = useRef(null);
  const map = useRef(null);
  const hasFitBounds = useRef(false);
  const stationPopup = useRef(null);
  const footprintPopup = useRef(null);

  // Initialize the map only once
  useEffect(() => {
    if (map.current) return;

    map.current = new maplibregl.Map({
      container: mapContainer.current,
      style: "https://basemaps.cartocdn.com/gl/positron-gl-style/style.json",
      center: [121.774, 12.8797],
      zoom: 5,
    });

    map.current.addControl(
      new maplibregl.NavigationControl(),
      "top-right"
    );

    stationPopup.current = new maplibregl.Popup({
      closeButton: true,
      closeOnClick: true,
    });

    footprintPopup.current = new maplibregl.Popup({
      closeButton: true,
      closeOnClick: true,
    });
  }, []);

  /* Render synoptic stations */
  useEffect(() => {

    if (!map.current) return;

    const renderStations = () => {

      updateStationLayer({
        map: map.current,
        stations: synopticStations,
        sourceId: "synoptic-source",
        layerId: "synoptic-layer",
        popup: stationPopup,
        otherPopup: footprintPopup,
        visible: showSynoptic,
      });

    };

    if (map.current.isStyleLoaded()) {
      renderStations();
    } else {
      map.current.once("load", renderStations);
    }

  }, [synopticStations, showSynoptic]);

  /* Render AWS stations */
  useEffect(() => {

    if (!map.current) return;

    const renderStations = () => {

      updateStationLayer({
        map: map.current,
        stations: awsStations,
        sourceId: "aws-source",
        layerId: "aws-layer",
        popup: stationPopup,
        otherPopup: footprintPopup,
        visible: showAWS,
      });

    };

    if (map.current.isStyleLoaded()) {
      renderStations();
    } else {
      map.current.once("load", renderStations);
    }

  }, [awsStations, showAWS]);

  /* Rendered footprints (Panahon) */
  useEffect(() => {

  if (!map.current || !footprints || footprints.features.length === 0) return;

  const renderFootprints = () => {

    updatePanahonLayer({
      map: map.current,
      sourceId: "panahon-footprints",
      fillLayerId: "panahon-fill",
      outlineLayerId: "panahon-outline",
      footprints: footprints,
      visible: showPanahonFootprints,
      hasFitBounds,
      stationPopup,
      footprintPopup,
    });

    if (map.current.getLayer("synoptic-layer")) {
      map.current.moveLayer("synoptic-layer");
    }

    if (map.current.getLayer("aws-layer")) {
      map.current.moveLayer("aws-layer");
    }

  };

  if (map.current.isStyleLoaded()) {
    renderFootprints();
  } else {
    map.current.once("load", renderFootprints);
  }

}, [footprints, showPanahonFootprints]);

/* Rendered footprints (ECMWF) */
  useEffect(() => {

  if (!map.current || !footprints || footprints.features.length === 0) return;

  const renderFootprints = () => {

    updateECMWFLayer({
      map: map.current,
      sourceId: "ecmwf-footprints",
      fillLayerId: "ecmwf-fill",
      outlineLayerId: "ecmwf-outline",
      footprints: footprints,
      visible: showEcmwfFootprints,
      hasFitBounds,
      stationPopup,
      footprintPopup,
    });

    if (map.current.getLayer("synoptic-layer")) {
      map.current.moveLayer("synoptic-layer");
    }

    if (map.current.getLayer("aws-layer")) {
      map.current.moveLayer("aws-layer");
    }

  };

  if (map.current.isStyleLoaded()) {
    renderFootprints();
  } else {
    map.current.once("load", renderFootprints);
  }

}, [footprints, showEcmwfFootprints]);

/* Rendered footprints (NASA GPM) */
  useEffect(() => {

  if (!map.current || !footprints || footprints.features.length === 0) return;

  const renderFootprints = () => {

    updateGPMLayer({
      map: map.current,
      sourceId: "gpm-footprints",
      fillLayerId: "gpm-fill",
      outlineLayerId: "gpm-outline",
      footprints: footprints,
      visible: showGpmFootprints,
      hasFitBounds,
      stationPopup,
      footprintPopup,
    });

    if (map.current.getLayer("synoptic-layer")) {
      map.current.moveLayer("synoptic-layer");
    }

    if (map.current.getLayer("aws-layer")) {
      map.current.moveLayer("aws-layer");
    }

  };

  if (map.current.isStyleLoaded()) {
    renderFootprints();
  } else {
    map.current.once("load", renderFootprints);
  }

}, [footprints, showGpmFootprints]);

/* Clean up when the component unmounts */
useEffect(() => {
  return () => {
    stationPopup.current?.remove();
    footprintPopup.current?.remove();
  };
}, []);

  return (
  <>

    <div
      ref={mapContainer}
      style={{
        width: "100%",
        height: "100%"
      }}
    />

  </>
);
}

export default MapView;
