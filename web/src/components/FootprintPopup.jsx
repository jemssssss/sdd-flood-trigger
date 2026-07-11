import { getLatestTimeDate, formatSensingTime } from "../utils/timeUtils";

function classify(mm) {
  if (mm > 180) return "Heavy";
  if (mm >= 60) return "Moderate";
  return "Light";
}

function FootprintPopup({ footprint }) {

  const SAMPLE_POINTS = Number(import.meta.env.VITE_SAMPLING_POINTS ?? 7);
  const panahon = Number(footprint.panahonRainfall ?? 0);
  const ecmwf = Number(footprint.ecmwfRainfall ?? 0);

  return (

    <div className="popup">

      <h3>Sentinel-1A Footprint</h3>

      <p>
        <strong>Tile</strong><br/>
        {footprint.TileNumber}
      </p>

      <p>
        <strong>Forecast Date</strong><br/>
        {getLatestTimeDate()}
      </p>

      <p>
        <strong>Sensing Time</strong><br/>
        {formatSensingTime()}
      </p>

      <p>
        <strong>Sampling Points (Panahon API)</strong><br/>
        {SAMPLE_POINTS}
      </p>

      <hr/>

      <h4>24-hour Rainfall</h4>

      <table>

        <tbody>

          <tr>
            <td>Panahon</td>
            <td>{panahon.toFixed(2)} mm</td>
          </tr>

          <tr>
            <td>ECMWF</td>
            <td>{ecmwf.toFixed(2)} mm</td>
          </tr>

        </tbody>

      </table>

      <hr/>

      <p>
        Not an observed flood extent
      </p>

    </div>

  );

}

export default FootprintPopup;