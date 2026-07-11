import "../styles/App.css";

function SummarySection({ title, summary }) {

  return (
    <div className="summary-section">

      <h4>{title}</h4>

      {/* Moderate */}

      <h5>
        Moderate Rainfall (60–180 mm)
      </h5>

      <p>
        {summary.moderate.length} Sentinel Tile(s)
      </p>

      {summary.moderate.length > 0 ? (

        <div className="tile-container">

          {summary.moderate.map(tile => (

            <span
              key={tile}
              className="tile-chip"
            >
              {tile}
            </span>

          ))}

        </div>

      ) : (

        <p className="empty-summary">
          None
        </p>

      )}

      {/* Heavy */}

      <h5>
        Heavy Rainfall (&gt;180 mm)
      </h5>

      <p>
        {summary.heavy.length} Sentinel Tile(s)
      </p>

      {summary.heavy.length > 0 ? (

        <div className="tile-container">

          {summary.heavy.map(tile => (

            <span
              key={tile}
              className="tile-chip"
            >
              {tile}
            </span>

          ))}

        </div>

      ) : (

        <p className="empty-summary">
          None
        </p>

      )}

    </div>
  );

}

function FloodSummary({
  panahonSummary,
  ecmwfSummary,
}) {

  return (

    <div className="flood-summary">

      <h3>
        Flood Trigger Summary
      </h3>

      <SummarySection
        title="Panahon API"
        summary={panahonSummary}
      />

      <SummarySection
        title="ECMWF Open Data"
        summary={ecmwfSummary}
      />

    </div>

  );

}

export default FloodSummary;