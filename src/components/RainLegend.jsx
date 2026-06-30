import "../styles/App.css";

function RainLegend() {
  const categories = [
    { color: "#d6eaf8", label: "No observed rain (0 mm)" },
    { color: "#aed6f1", label: "Light rainfall (1–10 mm)" },
    { color: "#5dade2", label: "Moderate rainfall (10–25 mm)" },
    { color: "#2874a6", label: "Heavy rainfall (25–50 mm)" },
    { color: "#154360", label: "Very heavy rainfall (>50 mm)" },
  ];

  return (
    <div className="rain-legend">
      <h3>Rainfall Legend</h3>

      {categories.map((category) => (
        <div className="legend-item" key={category.label}>
          <span
            className="legend-color"
            style={{ backgroundColor: category.color }}
          />
          <span>{category.label}</span>
        </div>
      ))}
    </div>
  );
}

export default RainLegend;