# Space Data Dashboard (SDD) Flood Trigger

A web-based rainfall visualization dashboard built with **React**, **Vite**, **MapLibre GL JS**, and a lightweight **Django backend**.

The application retrieves **Synoptic Station**, **Automatic Weather Station (AWS)**, and **Sentinel-1A footprint rainfall** from the **Panahon API** and **ECMWF Open Data** (via **earthkit-data API**) through backend service endpoints. Rainfall data from each source is processed independently before being visualized on the frontend. Sentinel footprint layers are pass-aware: only the strip scheduled to pass over the Philippines on the forecast date is processed and displayed. The architecture also provides the foundation for future **PostgreSQL/PostGIS** integration and additional Python-based geospatial services.

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
  - Automatic Weather Stations (AWS)
  - Sentinel-1A Passes
- Displays Sentinel-1A footprints only when a configured strip passes on the forecast date
- Computes 24-hour accumulated forecast rainfall from the Panahon API for every footprint in the passing strip
- Computes average 24-hour accumulated rainfall from ECMWF Open Data for every footprint in the passing strip
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
| Earthkit-data | 0.20.0 |
| Xarray | 2026.7.0 |
| NumPy | 2.5.1 |
| MapLibre GL JS | Latest compatible version |
| Turf.js | Latest compatible version |
| Requests | Latest compatible version |
| httpx | Latest compatible version |
| SciPy | Latest compatible version |
| GeoPandas | Latest compatible version |

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
VITE_SENSING_TIME=6
VITE_SAMPLING_POINTS=7
```

## Backend

```env
PANAHON_API_TOKEN=YOUR_API_TOKEN
```

`VITE_SENSING_TIME` and `VITE_SAMPLING_POINTS` are optional frontend display settings; the application uses `6` and `7` respectively when they are absent. Satellite selection does not require a frontend environment variable: the backend defaults to Sentinel-1A.

The Django settings read `PANAHON_API_TOKEN` from the backend process environment. In Windows Command Prompt, set it before starting Django:

```cmd
set PANAHON_API_TOKEN=YOUR_API_TOKEN
python manage.py runserver 127.0.0.1:8000
```

Obtain a valid Panahon API token from your project supervisor.

---

## Do NOT Commit the API Token

Ensure `.env` is ignored.

```gitignore
.env
```

A sample `.env.example` may be committed.

```env
VITE_BACKEND_BASE_URL=http://localhost:8000
VITE_SENSING_TIME=6
VITE_SAMPLING_POINTS=7
# Set PANAHON_API_TOKEN only in the backend runtime environment.
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
> The frontend calls the Django API; the Panahon API token remains on the backend. GitHub Pages can host only the static frontend, so production deployment requires a separately deployed Django API with HTTPS, CORS configuration, and `VITE_BACKEND_BASE_URL` set to that API URL at build time.

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
│   │   ├── dataset.py
│   │   ├── datetime.py
│   │   ├── footprint.py
│   │   ├── json_utils.py
│   │   └── sampler.py
│   │
│   ├── panahon/
│   │   ├── client.py
│   │   ├── footprint.py
│   │   ├── parser.py
│   │   └── point.py
│   │
│   └── sentinel/
│       └── passes.py
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
    │   │   ├── ecmwfTileLayer.jsx
    │   │   ├── panahonTileLayer.jsx
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
      Panahon API                 earthkit-data API
          │                               │
          └──────────────┬────────────────┘
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

## Current API Endpoints

The React app requests the following Django endpoints:

| Endpoint | Purpose |
|---|---|
| `GET /health/` | Backend health check |
| `GET /panahon/synoptic` | Normalized Synoptic station observations |
| `GET /panahon/aws` | Normalized AWS station observations |
| `GET /panahon/footprints?t=<forecast>&init=<initialization>` | Pass-filtered Sentinel footprint rainfall from Panahon |
| `GET /ecmwf/footprints?t=<forecast>&init=<initialization>` | Pass-filtered Sentinel footprint rainfall from ECMWF Open Data |

The legacy `/sentinel/footprints` route is currently an alias for the Panahon footprint route. New frontend code uses `/panahon/footprints`.

---

# Sentinel Pass Filtering

The backend uses the **forecast timestamp**, not the forecast initialization timestamp, to determine whether a configured satellite strip passes over the Philippines. For Sentinel-1A, each configured strip repeats every 12 days.

1. React sends `t` (forecast time) and `init` (forecast initialization time) to both footprint endpoints.
2. The backend checks the forecast date against the configured satellite pass schedule.
3. If a strip passes, only GeoJSON features whose `TileNumber` begins with that strip letter are sampled and returned.
4. If no strip passes, the API returns a valid empty GeoJSON `FeatureCollection`, empty summaries, and `passInfo`; no Panahon point requests or ECMWF download are performed.
5. The frontend shows the strip or **No Satellite Pass** and does not render empty footprint layers.

For example, a returned `passInfo` object has this shape:

```json
{
  "satellite": "Sentinel-1A",
  "passDate": "2026-07-18",
  "hasPass": true,
  "strip": "A"
}
```

Satellite schedules and footprint filenames are defined in `backend/services/sentinel/passes.py`. To add a future satellite such as Sentinel-1C, add its aliases, repeat period, strip reference dates, and GeoJSON filename to the `SATELLITES` registry after its footprint file is available. The Panahon and ECMWF services already resolve these values from the registry.

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

## Panahon Forecast Rainfall Sampling

Panahon Forecast rainfall is retrieved from:

```text
React
↓

GET /panahon/footprints?t=<forecast>&init=<initialization>

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

Forecast timestamps are generated automatically using `timeUtils.js`. The forecast timestamp determines the Sentinel strip; the initialization timestamp remains part of the rainfall forecast request.

---

## ECMWF Open Data Integration

The dashboard also supports rainfall visualization from ECMWF Open Data.

Rainfall is downloaded on demand using Earthkit-data and processed on the backend before being sent to the frontend.

Unlike the Panahon API, ECMWF rainfall is computed directly from the model raster.

Workflow:

```text
Earthkit

↓

Download GRIB

↓

Convert to Xarray

↓

Convert Total Precipitation to millimeters

↓

Extract rainfall values inside each Sentinel footprint

↓

Compute average rainfall

↓

Return GeoJSON to React
```

The backend automatically:

- downloads the requested forecast
- converts GRIB to Xarray
- filters to the scheduled Sentinel strip, then extracts rainfall inside its footprints
- computes average rainfall
- returns GeoJSON to the frontend

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

# Panahon API Field Mapping

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
- is included only when its strip is scheduled to pass on the forecast date

Below is a sample dashboard view when there is no satellite pass.

![No Satellite Pass Preview](/docs/no_pass.png)

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

## Panahon API

1. Load predefined sample points.
2. Request rainfall from the Panahon API.
3. Execute requests concurrently.
4. Cache repeated point requests.
5. Select the maximum sampled rainfall value for the footprint (stored in the existing `averageRainfall` property for compatibility).
6. Store as:

```javascript
feature.properties.averageRainfall
```

---

## ECMWF Open Data

1. Download the requested ECMWF forecast.
2. Convert GRIB to an Xarray dataset.
3. Convert total precipitation to millimeters.
4. Build a KD-tree from the ECMWF grid.
5. Find every raster cell intersecting the footprint.
6. Compute the arithmetic mean.
7. Fall back to the nearest grid cell if no raster cells intersect.
8. Store as:

```javascript
feature.properties.ecmwfRainfall
```

---

# Layer Controls

The dashboard includes a control panel that allows users to independently toggle:

- Synoptic Stations
- AWS Stations
- Footprints (Panahon)
- Footprints (ECMWF)

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
- Panahon API Forecast Rainfall (24 h)
- ECMWF Open Data Rainfall (24 h)

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
- For every footprint in the Sentinel strip scheduled for the forecast date:
  1. Django loads the satellite-specific footprint GeoJSON from the satellite registry.
  2. Django loads the predefined sampling points.
  3. Each sampling point requests 24-hour accumulated rainfall from the Panahon API.
  4. Results are cached to avoid duplicate requests.
  5. The maximum sampled Panahon rainfall value is selected.
  6. The average rainfall is stored in the GeoJSON feature.
  7. Flood summary tiles are generated.
  8. The completed GeoJSON is returned to React.
- Forecast timestamps are generated dynamically; the forecast timestamp determines the visible Sentinel strip.
- API responses are normalized before visualization.
- Environment variables are accessed using `import.meta.env`.
- Django serves as the backend API layer.
- Rainfall parsing has been migrated from React to Python.
- Footprint sampling is now performed on the backend.
- API tokens remain on the backend; `PANAHON_API_TOKEN` is read from the Django process environment.
- React now focuses primarily on visualization.
- Earthkit-data downloads ECMWF Open Data forecasts on demand.
- ECMWF rainfall is calculated directly from raster cells instead of sampling discrete points.
- KD-tree nearest-neighbor search is used as a fallback when a footprint does not intersect any ECMWF grid cell.
- Panahon API requests are executed concurrently using asyncio and httpx.
- Duplicate sampling points are automatically removed before requesting rainfall.
- Cached point requests reduce repeated API calls during subsequent refreshes.

---

# Backend Services

The Django backend currently provides lightweight API services for the frontend.

Implemented services include:

Panahon

- Synoptic endpoint
- AWS endpoint
- Point rainfall endpoint
- Sentinel footprint sampling endpoint

ECMWF

- Dataset endpoint
- Footprint rainfall endpoint
- Forecast datetime conversion service
- Earthkit dataset loader

These services simplify the frontend while preparing the project for future migration to database-backed processing.

The active Panahon footprint service is invoked by `apps/panahon/views.py`; Sentinel pass scheduling is provided by `services/sentinel/passes.py`. The `SATELLITES` registry also supplies the footprint GeoJSON filename, which keeps the active services ready for additional satellite datasets.

---

# Troubleshooting

## Missing API Token

```
PANAHON_API_TOKEN is not set
```

Verify:

- `.env` exists
- `PANAHON_API_TOKEN` is defined for the Django process
- the development server has been restarted

## No Footprints Displayed

First check the satellite pass status card. **No Satellite Pass** means the selected forecast date does not match a configured Sentinel strip, so empty Panahon and ECMWF footprint tables are expected. This is not a map-rendering error.

For Sentinel-1A, verify that the forecast date is one of the configured 12-day strip passes in `backend/services/sentinel/passes.py`. On a pass date, also verify that the matching `TileNumber` prefix is present in `web/public/data/s1a_footprints.geojson`.

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

## ECMWF Download Errors

Possible causes:

- corrupted local Earthkit cache
- interrupted GRIB download
- temporary ECMWF Open Data service issue

Recommended fixes:

- clear the Earthkit cache
- retry the request
- verify the requested forecast initialization time exists

---

## Panahon API Rate Limiting

```text
429 Too Many Requests
```

Possible cause:

- too many simultaneous point requests

Recommended fixes:

- reduce the number of sampling points
- reduce concurrent requests
- rely on backend caching for repeated requests

---

## Incorrect Panahon Rainfall (All Zero)

Verify:

- forecast timestamp exists
- initialization timestamp matches the forecast
- Panahon API returns non-zero rainfall for the requested period
- cached responses are not stale
- sampling coordinates are valid

---
