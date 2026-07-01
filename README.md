# Space Data Dashboard (SDD) Flood Trigger

A web-based rainfall monitoring dashboard built with **React**, **Vite**, and **MapLibre GL JS**. The application retrieves real-time rainfall station data from the **Panahon API**, normalizes the raw response into a consistent data model, and visualizes rainfall observations on an interactive map.

> **Note:** This application visualizes **rainfall observations only**. It does **not** represent flood extent, flood susceptibility, or flood risk.

---

## Features

- Interactive MapLibre map centered on the Philippines
- Fetches rainfall station data from the Panahon API
- Normalizes raw API data into a consistent station object format
- Loading, error, and empty states during data retrieval
- Rainfall visualization using colored and sized point symbols
- Interactive station pop-ups displaying:
  - Station name
  - Rainfall amount
  - Observation time
  - Coordinates
- Rainfall legend based on rainfall intensity categories

---

## Tech Stack

| Technology | Version |
|------------|---------|
| Node.js | v22.20.0 |
| npm | 10.9.3 |
| Vite | 8.1.0 |
| React | 19.2.7 |
| MapLibre GL JS | Latest compatible version |

---

## Prerequisites

Before running the project, ensure the following are installed:

- Node.js (v22.20.0 or later recommended)
- npm (v10.9.3 or later)

Verify your installation:

```bash
node -v
npm -v
```

---

## Project Setup

Clone the repository:

```bash
git clone https://github.com/jemssssss/sdd-flood-trigger.git
cd sdd-flood-trigger
```

---

## Environment Variables

The application requires a Panahon API token.

Create a `.env` file in the project root:

```env
VITE_PANAHON_API_TOKEN=YOUR_API_TOKEN
```

> Obtain a **Panahon API token** from your project supervisor before running the application.

### Do NOT commit your API token

The `.env` file should be listed in `.gitignore`:

```gitignore
.env
```

A sample `.env.example` file may be committed for reference:

```env
VITE_PANAHON_API_TOKEN=
```

---

## Installation

Install project dependencies:

```bash
npm install
```

---

## Running the Application

Start the Vite development server:

```bash
npm run dev
```

Open your browser and navigate to:

```
http://localhost:5173
```

---

## Project Structure

```text
src/
├── components/
│   ├── MapView.jsx
│   ├── RainLegend.jsx
│   └── RainStationPopup.jsx
│
├── services/
│   └── panahonApi.js
│
├── utils/
│   └── rainParser.js
│
├── styles/
│   ├── App.css
│   └── index.css
│
├── App.jsx
└── main.jsx
```

---

## Application Flow

```text
Panahon API
      │
      ▼
fetchRainSynop()
      │
      ▼
Raw API Response
      │
      ▼
parseRainStations()
      │
      ▼
Normalized Station Objects
      │
      ▼
App.jsx
      │
      ▼
MapView.jsx
      │
      ▼
MapLibre GeoJSON Layer
      │
      ▼
Rainfall Visualization & Pop-ups
```

---

## Panahon API Integration

The application retrieves rainfall observations from the Panahon API.

Example endpoint:

```text
https://www.panahon.gov.ph/api/v1/synop?token=<TOKEN>&parameter=rain
```

---

## Raw API Response

Example:

```json
{
  "success": true,
  "data": [
    {
      "site_id": "132",
      "site_name": "ITBAYAT, BATANES",
      "lat": "20.79000758",
      "lon": "121.8396475",
      "value": "0",
      "parameter": "rain",
      "observed_at": "2026-06-30 14:00:00",
      "readable_parameter": "3 Hourly Rain",
      "readable_unit": "mm"
    }
  ]
}
```

---

## Normalized Station Object

The raw API response is converted into a standardized object before visualization.

Example:

```javascript
{
  id: "132",
  stationName: "ITBAYAT, BATANES",
  latitude: 20.79000758,
  longitude: 121.8396475,
  rainfallMm: 0,
  observedAt: "2026-06-30 14:00:00",
  raw: { ... }
}
```

---

## API Field Mapping

| Panahon API Field | Parsed Field | Notes |
|-------------------|--------------|-------|
| `site_id` | `id` | Unique station identifier |
| `site_name` | `stationName` | Rainfall station name |
| `lat` | `latitude` | Latitude coordinate |
| `lon` | `longitude` | Longitude coordinate |
| `value` | `rainfallMm` | Rainfall amount (**millimeters (mm)**) |
| `observed_at` | `observedAt` | Observation timestamp |

The original API object is preserved in the `raw` property for future use.

---

## Rainfall Visualization

Rainfall stations are displayed as circle symbols on the map.

Both **color** and **circle size** represent rainfall intensity.

| Rainfall (mm) | Category | Visualization |
|--------------:|----------|---------------|
| 0 | No observed rain | Smallest, lightest blue |
| 1–10 | Light rainfall | Slightly larger, light blue |
| 10–25 | Moderate rainfall | Medium-sized, medium blue |
| 25–50 | Heavy rainfall | Large, dark blue |
| >50 | Very heavy rainfall | Largest, darkest blue |

> The visualization represents **rainfall observations only**.

---

## Pop-up Information

Clicking a rainfall station displays a pop-up containing:

- Station name
- Rainfall amount (mm)
- Observation time
- Latitude
- Longitude

---

## Loading States

The application provides clear feedback while fetching data.

- **Loading** – Displayed while requesting data from the API.
- **Error** – Displayed if the API request fails.
- **Empty State** – Displayed when no rainfall stations are available.

---

## Development Notes

- React is responsible for application state and UI.
- MapLibre handles map rendering.
- Rainfall stations are rendered as a GeoJSON source and circle layer.
- API responses are normalized before reaching the map component.
- Environment variables are accessed through `import.meta.env`.

---

## Troubleshooting

### Missing API Token

```
Missing VITE_PANAHON_API_TOKEN
```

Ensure that:

- `.env` exists
- `VITE_PANAHON_API_TOKEN` is defined
- The development server has been restarted after modifying `.env`

---

### Style is not done loading

```
Style is not done loading.
```

This occurs when attempting to add a MapLibre source or layer before the map style has finished loading.

Ensure that sources and layers are added only after the map's `load` event.

---

### No Rainfall Stations Displayed

Verify:

- The API token is valid.
- The API request succeeds.
- Parsed stations contain valid latitude and longitude values.
- Browser Developer Tools (Console and Network tabs) do not report errors.

