function FootprintPopup({ footprint }) {

  return (
    <div className="popup">

      <h3>Sentinel-1 Footprint</h3>

      <p>
        <strong>Tile:</strong><br />
        {footprint.TileNumber}
      </p>

      <p>
        <strong>Average Rainfall:</strong><br />
        {Number(footprint.averageRainfall).toFixed(2)} mm
      </p>

    </div>
  );

}

export default FootprintPopup;