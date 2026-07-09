# Space Data Dashboard (SDD) Flood Trigger

A web-based rainfall visualization dashboard built with **React**, **Vite**, **MapLibre GL JS**, and a lightweight **Django backend**.

The application retrieves **Synoptic Station**, **Automatic Weather Station (AWS)**, and **Sentinel-1A footprint rainfall** from the **Panahon API** through backend service endpoints. The backend also provides the foundation for future **ECMWF Open Data**, **PostgreSQL/PostGIS**, and additional Python-based geospatial services.

![SDD Flood Trigger Preview](/docs/dashboard_preview.png)

> **Note**
>
> This application visualizes **rainfall observations and forecast rainfall only**. It does **not** represent flood extent, flood susceptibility, or flood risk.

---

# Features

- Interactive MapLibre map centered on the Philippines
- Displays Synoptic Station rainfall observations (3-hour accumulated rainfall)
- Displays AWS rainfall observations (24-hour accumulated rainfall)
- Layer control panel for toggling:
  - Synoptic Stations
  - AWS Stations
  - Sentinel-1A Footprints
- Displays Sentinel-1 footprint polygons
- Computes average 24-hour accumulated forecast rainfall for every footprint
- Uses pre-generated sampling points for reproducible rainfall averaging
- Summarizes list of Sentinel-1A tiles showing signs of flooding
- Color-coded rainfall stations
- Color-coded footprint polygons
- Interactive station popups
- Interactive footprint popups
- Rainfall legend
- Loading, error, and empty states
- Django backend API layer
- Backend proxy for Panahon API requests
- Backend Sentinel footprint sampling service
- Backend rainfall parsing service
- Cached point rainfall requests
- Designed for future ECMWF Open Data integration
- Prepared for PostgreSQL/PostGIS integration

---

# Tech Stack

| Technology | Version |
|------------|---------|
| Node.js | v22.20.0 |
| npm | 10.9.3 |
| Vite | 8.1.0 |
| React | 19.2.7 |
| Python | 3.13.14 |
| Django | 6.0.7 |
| MapLibre GL JS | Latest compatible version |
| Turf.js | Latest compatible version |
| Requests | Latest compatible version |
| httpx | Latest compatible version |

---

# Prerequisites

Install:

- Node.js (v22.20.0 or newer recommended)
- npm (v10.9.3 or newer)

Verify installation:

```bash
node -v
npm -v
```

---

# Project Setup

Clone the repository.

```bash
git clone https://github.com/jemssssss/sdd-flood-trigger.git

cd sdd-flood-trigger
```

---

## Development setup

This repository now has two parts:

- `web/` - React + Vite + MapLibre frontend
- `backend/` - Django backend

### Run the web app

```cmd
cd web
npm install
npm run dev
```

Open:

```text
http://localhost:5173
```

### Run the backend

```cmd
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py runserver 127.0.0.1:8000
```

Open:

```text
http://localhost:8000/health/
```

---

# Environment Variables

Create a `.env` file.

## Frontend

```env
VITE_BACKEND_BASE_URL=http://localhost:8000
SENSING_TIME=sensing_time_here
SAMPLING_POINTS=sample_points_here
```

## Backend

```env
PANAHON_API_TOKEN=YOUR_API_TOKEN
```

Sensing time and sampling points are variables that can be changed according to the user's needs.

Obtain a valid Panahon API token from your project supervisor.

---

## Do NOT Commit the API Token

Ensure `.env` is ignored.

```gitignore
.env
```

A sample `.env.example` may be committed.

```env
VITE_PANAHON_API_TOKEN=
SENSING_TIME=
SAMPLING_POINTS=
```

---

# Installation

Install dependencies.

```bash
npm install
```

---

# Running the Application

```bash
npm run dev
```

Open:

```
http://localhost:5173
```

---

# Deploying to GitHub Pages

Deploy using:

```bash
npm run deploy
```

The project is configured to deploy from the **gh-pages** branch.

> **Note**
>
> Since this application currently performs API requests entirely on the frontend, the Panahon API token is included in the production bundle. A backend proxy is recommended for production deployments.

---

# Project Structure

```text
backend/
├── apps/
│   ├── core/
│   │   ├── urls.py
│   │   └── views.py
│   │
│   ├── ecmwf/
│   │   ├── urls.py
│   │   └── views.py
│   │
│   └── panahon/
│       ├── urls.py
│       └── views.py
│
├── config/
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── services/
│   ├── ecmwf/
│   │   └── point.py
│   │
│   ├── panahon/
│   │   ├── client.py
│   │   └── parser.py
│   │
│   └── sentinel/
│       ├── footprint.py
│       └── point.py
│       
├── manage.py
└── requirements.txt

web/
├── public/
│   └── data/
│       ├── s1a_footprints.geojson
│       └── footprintSamplePoints.json
│    
└── src/
    ├── components/
    │   ├── map/
    │   │   ├── footprintLayer.jsx
    │   │   └── stationLayer.jsx
    │   │
    │   ├── EcmwfPointTest.jsx
    │   ├── LayerControl.jsx
    │   ├── FloodSummary.jsx
    │   ├── FootprintPopup.jsx
    │   ├── MapView.jsx
    │   ├── RainLegend.jsx
    │   ├── StationLayer.jsx
    │   └── StationPopup.jsx
    │
    ├── services/
    │   └── ecmwfApi.jsx
    │
    ├── utils/
    │   ├── generateFootprintPoints.mjs
    │   └── timeUtils.js
    │
    ├── styles/
    │   ├── App.css
    │   └── index.css
    │
    ├── App.jsx
    └── main.jsx
```

---

# Application Workflow

```text
                    Panahon API
                         │
                         ▼
                Django Backend Services
         ┌───────────────┼────────────────┐
         │               │                │
         ▼               ▼                ▼
   Station Client   Point Sampling   Footprint Service
         │               │                │
         └───────────────┼────────────────┘
                         │
                  JSON API Endpoints
                         │
                         ▼
                 React + Vite Frontend
                         │
                         ▼
                    MapLibre GL JS
```

---

# Panahon API Integration

## Synoptic Stations

Observed rainfall stations:

```text
React
↓

GET /panahon/synoptic

↓

Django

↓

Panahon API
```

Represents **3-hour accumulated rainfall**.

---

## Automatic Weather Stations (AWS)

Observed AWS stations:

```text
React
↓

GET /panahon/aws

↓

Django

↓

Panahon API
```

Represents **24-hour accumulated rainfall**.

Although the endpoint returns hourly rainfall, this dashboard visualizes the **24_hr_value** field.

---

## Forecast Rainfall Sampling

Forecast rainfall is retrieved from:

```text
React
↓

GET /sentinel/footprints

↓

Django

↓

Panahon API
```

using:

- latitude
- longitude
- forecast timestamp
- API token

Forecast timestamps are generated automatically using `timeUtils.js`.

---

# Rainfall Station Types

## Synoptic Stations

Visualized using:

- `value`
- 3-hour rainfall
- rainfall station popup

---

## AWS Stations

Visualized using:

- `24_hr_value`
- 24-hour accumulated rainfall
- identical popup layout

---

# Raw API Response

Example Synoptic rainfall station response:

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

Example AWS rainfall station response:

```json
{
	"success":true,
	"data": [
		{
			"site_id":"98",
			"site_name":"Science Garden, Quezon City",
			"lat":14.645101,
			"lon":121.044258,
			"parameter":"accumulated_rain_1h",
			"readable_parameter":"Hourly Rain",
			"readable_unit":"mm",
			"observed_at":"2026-07-06 14:40:00",
			"value":"0",
			"24_hr_value":"0"
		}
	]
}	
```

Example footprint sample point response:

```json
{
  "coordinates": [118.480028433565, 6.99440848821885],
  "values": [1.7]
}
```

---

# Normalized Rainfall Station Object

Before visualization, the API response is converted into a standardized format.

Example normalized Synoptic rainfall station response:

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

Example normalized AWS rainfall station response:

```javascript
{
  id: "98",
  latitude: 14.645101,
  longitude: 121.044258,
  rainfallMm: 0,
  observedAt: "2026-06-30 14:00:00",
  raw: { ... },
	readableUnit: "mm",
	stationName: "Science Garden, Quezon City",
	stationType: "aws"
}
```

---

# API Field Mapping

| Panahon API | Parsed Field | Description |
|-------------|--------------|-------------|
| `site_id` | `id` | Station identifier |
| `site_name` | `stationName` | Station name |
| `lat` | `latitude` | Latitude |
| `lon` | `longitude` | Longitude |
| `value` | `rainfallMm` | Rainfall amount (millimeters) |
| `observed_at` | `observedAt` | Observation timestamp |

The original API response is preserved in the `raw` property.

---

# Sentinel-1A Footprints

Sentinel-1A acquisition footprints are loaded from:

```
public/data/s1a_footprints.geojson
```

Each footprint:

- displays forecasted total rainfall accumulated over the past 24 hours from sensing time
- is color-coded
- supports interactive popups

---

# Sampling Points

Each footprint uses pre-generated sample coordinates stored in:

```
public/data/footprintSamplePoints.json
```

Advantages:

- deterministic results
- improved performance
- reproducible averages
- easy increase in sampling density

---

# Average Rainfall Computation

For every footprint:

1. Load predefined sample points.
2. Fetch rainfall at every point.
3. Execute requests concurrently.
4. Compute the arithmetic mean.
5. Store as:

```javascript
feature.properties.averageRainfall
```

---

# Layer Controls

The dashboard includes a control panel that allows users to independently toggle:

- Synoptic Stations
- AWS Stations
- Sentinel-1A Footprints

Layer visibility is managed using MapLibre's `layout.visibility` property without reloading map sources.

---

# Station Popups

Clicking either a Synoptic or AWS station displays:

- Station name
- Rainfall amount
- Observation time
- Latitude
- Longitude

![Synoptic Station Popup](/docs/synoptic_popup.png)

![AWS Station Popup](/docs/aws_popup.png)

The rainfall label automatically changes depending on station type:

- Synoptic → **Rainfall (3h)**
- AWS → **Rainfall (24h)**

---

# Footprint Popups

Clicking a Sentinel-1A footprint displays:

- Sentinel Tile Number
- Forecasted Date
- Sensing Time (AM/PM)
- Sampling Points Used
- Forecast Accumulated Rainfall (mm)

![Sentinel-1A Footprint Popup](/docs/footprint_popup.png)

---

# Loading States

The application provides feedback during data retrieval.

- Loading
- Error
- Empty state

---

# Development Notes

- React manages application state.
- MapLibre GL JS renders all spatial layers.
- Layer rendering has been modularized into dedicated map layer components.
- Turf.js generated the initial sampling points.
- Sampling points are reused between application runs.
- For every Sentinel-1A footprint:
  1. Django loads the footprint GeoJSON.
  2. Django loads the predefined sampling points.
  3. Each sampling point requests 24-hour accumulated rainfall from the Panahon API.
  4. Results are cached to avoid duplicate requests.
  5. The arithmetic mean is computed.
  6. The average rainfall is stored in the GeoJSON feature.
  7. Flood summary tiles are generated.
  8. The completed GeoJSON is returned to React.
- Forecast timestamps are generated dynamically.
- API responses are normalized before visualization.
- Environment variables are accessed using `import.meta.env`.
- Django serves as the backend API layer.
- Rainfall parsing has been migrated from React to Python.
- Footprint sampling is now performed on the backend.
- API tokens remain on the backend.
- React now focuses primarily on visualization.

---

# Backend Services

The Django backend currently provides lightweight API services for the frontend.

Implemented services include:

- Health endpoint
- Panahon Synoptic endpoint
- Panahon AWS endpoint
- Panahon Point Rainfall endpoint
- Panahon Sentinel Footprint Sampling endpoint

These services simplify the frontend while preparing the project for future migration to database-backed processing.

---

# Troubleshooting

## Missing API Token

```
Missing VITE_PANAHON_API_TOKEN
```

Verify:

- `.env` exists
- the token is defined
- the development server has been restarted

---

## Style is not done loading

```
Style is not done loading
```

Ensure MapLibre sources and layers are only added after the map's `load` event.

---

## GitHub Pages Displays a Blank Page

Verify:

- `vite.config.js` contains the correct `base` path
- assets use `import.meta.env.BASE_URL`
- GitHub Pages is configured to deploy from the `gh-pages` branch
- redeploy using:

```bash
npm run deploy
```

---

## No Stations Displayed

Verify:

- the API token is valid
- the Panahon API requests succeed
- valid coordinates are returned
- browser Developer Tools report no JavaScript errors

---

## Incorrect Footprint Rainfall

Verify:

- the generated forecast timestamp matches the latest available forecast
- `footprintSamplePoints.json` contains valid coordinates
- the Panahon forecast endpoint returns valid values

---