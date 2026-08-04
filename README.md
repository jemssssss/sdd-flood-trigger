# Space Data Dashboard (SDD) Flood Trigger

A web-based rainfall visualization dashboard built with **React**, **Vite**, **MapLibre GL JS**, and a lightweight **Django backend**.

The application retrieves **Synoptic Station**, **Automatic Weather Station (AWS)**, and **Sentinel-1 satellite footprint rainfall** from the **Panahon API**, **ECMWF Open Data** (via **Earthkit API**), and **NASA GPM IMERG** (via **Earthaccess API**) through backend service endpoints. Rainfall data from each source is processed independently before being visualized on the frontend. Sentinel-1 satellite footprint layers are pass-aware: only the strip scheduled to pass over the Philippines on the forecast datetime is processed and displayed. The architecture also provides the foundation for future **PostgreSQL/PostGIS** integration and additional Python-based geospatial services.

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
  - Panahon API Forecast Data
  - ECMWF Forecast Data
  - NASA GPM IMERG Observational Data
- Displays Sentinel-1A or Sentinel-1C footprints only when a configured strip passes on the forecast date
- Computes 24-hour accumulated forecast rainfall from Panahon API for every footprint in the passing strip
- Computes 24-hour accumulated forecast rainfall from ECMWF Open Data for every footprint in the passing strip
- Computes 24-hour accumulated forecast rainfall from NASA GPM IMERG for every footprint in the passing strip
- Uses pre-generated sampling points via Poisson disk sampling (specifically for Panahon API) for reproducible rainfall averaging
- Summarizes list of Sentinel-1 satellite footprints showing signs of flooding
- Color-coded rainfall stations
- Color-coded footprint polygons
- Interactive station popups
- Interactive footprint popups
- Rainfall legend
- Loading, error, and empty states
- Django backend API layer
- Backend proxy for API requests
- Backend Sentinel-1 satellite footprint sampling service
- Backend rainfall parsing service
- Cached point rainfall requests
- Cached downloaded GRIB/HDF5 files from Earthkit and Earthaccess APIs
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
| python-dotenv | 1.2.2 |
| Django | 6.0.7 |
| earthkit-data | 0.20.0 |
| earthaccess | 0.18.0 |
| Xarray | 2026.7.0 |
| NumPy | 2.5.1 |
| SciPy | 1.18.0 |
| Shapely | 2.1.2 |
| GeoPandas | 1.1.4 |
| Requests | 2.34.2 |
| httpx | 0.28.1 |
| MapLibre GL JS | Latest compatible version |
| Turf.js | Latest compatible version |
| Poisson Disk Sampling | Latest compatible version |


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

This repository has two parts:

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
VITE_PANAHON_API_TOKEN=your_token_here
VITE_BACKEND_BASE_URL=http://localhost:8000
SAMPLING_POINTS=sample_points_here
```

## Backend

```env
EARTHDATA_USERNAME=your_username
EARTHDATA_PASSWORD=your_password
```

Satellite selection does not require a frontend environment variable: the backend defaults to Sentinel-1A.

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
├── data/
│   ├── earthkit_cache/
│   └── gpm_cache/
│
├── scripts/
│   └── json_utils.py
│
├── services/
│   ├── ecmwf/
│   │   ├── datetime.py
│   │   ├── footprint.py
│   │   └── sampler.py
│   │
│   ├── gpm/
│   │   ├── dataset.py
│   │   ├── datetime.py
│   │   ├── footprint.py
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
│       ├── s1c_footprints.geojson
│       ├── footprintSamplePoints.json
│       └── footprintSamplePoints_C.json
│    
└── src/
    ├── components/
    │   ├── map/
    │   │   ├── ecmwfTileLayer.jsx
    │   │   ├── gpmTileLayer.jsx
    │   │   ├── panahonTileLayer.jsx
    │   │   └── stationLayer.jsx
    │   │
    │   ├── LayerControl.jsx
    │   ├── FloodSummary.jsx
    │   ├── FootprintPopup.jsx
    │   ├── MapView.jsx
    │   ├── RainLegend.jsx
    │   ├── StationLayer.jsx
    │   └── StationPopup.jsx
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
                    Panahon API   Earthaccess API   Earthkit API
                          │              │              │
                          └──────────────┼──────────────┘
                                         │
                                         ▼
                              Django Backend Services
         ┌────────────────────┬──────────┴──────────┬─────────────────────┐
         │                    │                     │                     │
         ▼                    ▼                     ▼                     ▼ 
  Station Client        Point Sampling      Footprint Service   Sentinel-1 Strip Service
         │                    │                     │                     │
         └────────────────────┴──────────┬──────────┴─────────────────────┘
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
| `GET /panahon/footprints` | Pass-filtered Sentinel-1 satellite footprint rainfall from Panahon |
| `GET /ecmwf/footprints` | Pass-filtered Sentinel-1 satellite footprint rainfall from ECMWF Open Data |
| `GET /gpm/footprints` | Pass-filtered Sentinel-1 satellite footprint rainfall from NASA GPM IMERG |

---

# Sentinel-1 Satellite Pass Filtering

The backend uses the **forecast timestamp**, not the initialization timestamp, to determine whether a configured satellite strip passes over the Philippines. For Sentinel-1A and Sentinel-1C, each configured strip repeats every 12 days.

1. React requests footprint endpoints, then Django backend obtains current forecast and initial datetimes.
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

Satellite schedules and footprint filenames are defined in `backend/services/sentinel/passes.py`. To add a future satellite, add its aliases, repeat period, strip reference dates, and GeoJSON filename to the `SATELLITES` registry after its footprint file is available. The Panahon, ECMWF, and NASA GPM services already resolve these values from the registry.

---

# Sentinel-1 Satellite Footprints

Sentinel-1A and Sentinel-1C acquisition footprints are loaded from:

```
web/public/data/s1a_footprints.geojson
web/public/data/s1c_footprints.geojson
```

Each footprint:

- displays forecasted total rainfall accumulated over the past 24 hours from sensing time
- is color-coded
- supports interactive popups
- is included only when its strip is scheduled to pass on the forecast date

Below is a sample dashboard view when there is no satellite pass.

![No Satellite Pass Preview](/docs/no_pass.png)

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

Visualized using:

- `value`
- 3-hour rainfall
- rainfall station popup

### API Response

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

### Normalized Response

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

Visualized using:

- `24_hr_value`
- 24-hour accumulated rainfall
- identical popup layout

### API Response

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

### Normalized Response

Before visualization, the API response is converted into a standardized format.

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

## Rainfall Station API Field Mapping

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

## Footprint Forecast Rainfall Sampling

Panahon Forecast rainfall is retrieved from:

```text
React
↓

GET /panahon/footprints

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

Forecast timestamps are generated automatically from `backend/services/sentinel/passes.py`. The forecast timestamp determines the Sentinel-1 satellite strip; the initialization timestamp remains part of the rainfall forecast request.

### API Response

Example footprint sample point response:

```json
{
  "coordinates": [118.480028433565, 6.99440848821885],
  "values": [1.7]
}
```

### Sampling Points

Each footprint uses pre-generated sample coordinates stored in:

```
web/public/data/footprintSamplePoints.json
web/public/data/footprintSamplePoints_C.json
```

Advantages:

- deterministic results
- improved performance
- reproducible averages
- easy increase in sampling density

### Average Rainfall Computation

For every footprint:

1. Load predefined sample points.
2. Request rainfall from the Panahon API.
3. Execute requests concurrently.
4. Cache repeated point requests.
5. Compute the average rainfall value for the footprint (stored in the existing `averageRainfall` property for compatibility).
6. Store as:

```javascript
feature.properties.averageRainfall
```

---

# ECMWF Open Data Integration

The dashboard also supports rainfall visualization from ECMWF's **Open Data** dataset.

24-hour accumulated total precipitation (tp) from the ECMWF Open Data service is downloaded on demand using earthkit-data and processed on the backend before being sent to the frontend.

## Footprint Raster Sampling

Unlike the Panahon API, ECMWF rainfall is computed directly from the model raster.

Workflow:

```text
earthkit-data

↓

Download GRIB

↓

Convert to Xarray

↓

Convert Total Precipitation (tp) to millimeters

↓

Extract rainfall values inside each Sentinel-1 satellite footprint

↓

Compute average rainfall

↓

Return GeoJSON to React
```

The backend automatically:

- downloads the requested forecast
- converts GRIB to Xarray
- filters to the scheduled Sentinel-1 satellite strip, then extracts rainfall inside its footprints
- computes average rainfall
- returns GeoJSON to the frontend

## Downloading ECMWF Open Data using earthkit-data

The ECMWF forecast is downloaded using the `earthkit-data` library defined in `backend/services/ecmwf/sampler.py`.

Here's an example request field for obtaining the total precipitation (tp):

```python
ds = ek.from_source(
    "ecmwf-open-data",
    request={
        "type": "fc",
        "stream": "oper",
        "levtype": "sfc",
        "param": "tp",
        "date": "20260719",
        "time": "0600",
        "step": 24
    }
)
```

| Parameter | Description |
|-----------|-------------|
| `type="fc"` | Forecast product |
| `stream="oper"` | Operational forecast |
| `levtype="sfc"` | Surface variables |
| `param="tp"` | Total precipitation |
| `date` | Forecast initialisation date (UTC) |
| `time` | Forecast initialisation time (UTC) |
| `step=24` | 24-hour accumulated precipitation forecast |

The downloaded dataset is provided as a GRIB file, which is automatically converted into an `xarray.Dataset` by earthkit.

> **Note**
>
> ECMWF Open Data only accepts time values set at 12AM, 6AM, 12PM, and 6PM (in UTC). Furthermore, it only accepts step values in increments of 24.

## Building the Spatial Index

The ECMWF rainfall grid consists of regularly spaced latitude and longitude coordinates.

The script first generates all grid-point coordinates:

```python
lon_grid, lat_grid = np.meshgrid(longitudes, latitudes)
```

The coordinate arrays are flattened into a list of longitude-latitude pairs:

```python
coords = np.column_stack((
    lon_grid.ravel(),
    lat_grid.ravel()
))
```

A KD-tree is then created:

```python
tree = cKDTree(coords)
```

The KD-tree enables fast nearest-neighbour searches, which are used as a fallback when a footprint contains no ECMWF grid points.

## Average Rainfall Computation

For each footprint:

1. Computes the polygon's bounding box.
2. Finds all ECMWF grid points inside the bounding box.
3. Checks whether each candidate point lies inside the footprint.
4. Collects the rainfall values for those grid points.
5. Computes the arithmetic mean.
6. Store as:

```javascript
feature.properties.ecmwfRainfall
```

Restricting the search to the bounding box significantly reduces the number of point-in-polygon tests compared to checking every ECMWF grid point.

---

# NASA GPM IMERG Integration

The dashboard also supports rainfall visualization from NASA's **Global Precipitation Measurement (GPM) Integrated Multi-satellite Retrievals for GPM (IMERG)**.

24-hour accumulated rainfall is computed from the **IMERG Early Half-Hourly V07** product downloaded through `earthaccess`. The backend accumulates 48 half-hourly precipitation fields before computing the average rainfall over each Sentinel-1 satellite footprint.

## Footprint Raster Sampling

Unlike the Panahon API, GPM rainfall is computed directly from the IMERG raster.

Workflow:

```text
earthaccess

↓

Search IMERG Half-Hourly granules

↓

Download 48 HDF5 files

↓

Open each file using Xarray

↓

Convert precipitation rate to rainfall accumulation

↓

Build 24-hour accumulated rainfall raster

↓

Extract rainfall values inside each Sentinel-1 satellite footprint

↓

Compute average rainfall

↓

Return GeoJSON to React
```

The backend automatically:

- searches for the required IMERG Half-Hourly granules
- downloads (or reuses cached) HDF5 files
- builds a 24-hour accumulated rainfall raster
- filters to the scheduled Sentinel-1 satellite strip, then extracts rainfall inside its footprints
- computes average rainfall
- returns GeoJSON to the frontend

## Downloading IMERG Half-Hourly using earthaccess

The IMERG data is downloaded using the `earthaccess` library defined in `backend/services/gpm/dataset.py`.

Here's an example search request:

```python
granules = earthaccess.search_data(
    short_name="GPM_3IMERGHHE",
    temporal=(
        init_time.isoformat(),
        forecast_time.isoformat(),
    ),
)
```

The returned granules are downloaded locally using:

```python
earthaccess.download(
    granules,
    local_path=DOWNLOAD_DIR,
)
```

| Parameter | Description |
|-----------|-------------|
| `short_name="GPM_3IMERGHHE"` | IMERG Early Half-Hourly Version 07 product |
| `temporal` | 24-hour search interval between the initialization time and forecast time |

Unlike the Daily IMERG product, the Half-Hourly product returns one HDF5 file every 30 minutes. A complete 24-hour accumulation therefore consists of **48 granules**.

> **Note**
>
> IMERG Early data is typically available approximately **5 hours behind UTC real time**. Requests newer than the latest available product are rejected by the backend.

## Earthdata Login

NASA GPM IMERG data is distributed through the **NASA Earthdata** system, which requires user authentication before any datasets can be searched or downloaded.

The backend performs authentication using the `earthaccess` library. Login credentials are stored as environment variables and are loaded at runtime using `python-dotenv`.

The login routine is implemented in `backend/services/gpm/dataset.py`:

```python
from dotenv import load_dotenv
import earthaccess

load_dotenv()

earthaccess.login(
    strategy="environment",
    persist=False,
)
```

The required environment variables are stored in the backend `.env` file:

```text
EARTHDATA_USERNAME=your_username
EARTHDATA_PASSWORD=your_password
```

The `environment` authentication strategy instructs `earthaccess` to read these credentials directly from the environment instead of prompting the user interactively.

Using

```python
persist=False
```

prevents Earthaccess from saving authentication credentials to the local machine, allowing every dashboard instance to authenticate only for the current application session.

To avoid repeated authentication during the lifetime of the backend process, the service maintains a simple login flag:

```python
_logged_in = False
```

The login function first checks whether authentication has already been completed:

```python
if _logged_in:
    return
```

If the user has already authenticated, subsequent requests immediately reuse the existing Earthdata session without performing another login request.

This approach provides two advantages:

- only one authentication request is sent to the Earthdata servers during the application's lifetime;
- subsequent IMERG downloads can begin immediately without incurring additional login overhead.

> **Note**
>
> Before using this feature, an Earthdata account must first be created and granted access to the GPM IMERG datasets. Authentication is mandatory even though the IMERG Early products are publicly available through NASA. A free account is sufficient for the scope of this project, which can be made here: `https://urs.earthdata.nasa.gov/`

## Building the 24-Hour Rainfall Accumulation

Each IMERG Half-Hourly file stores precipitation as a rainfall rate in **millimetres per hour (mm/hr)**.

The rainfall layer is extracted from the `Grid` group of each HDF5 file:

```python
ds = xr.open_dataset(
    file,
    engine="netcdf4",
    group="Grid",
)

rain = ds["precipitation"].isel(time=0)
```

Each file represents rainfall over a 30-minute interval.

The rainfall accumulation contributed by each file is therefore computed as:

```python
rain_mm = rain * 0.5
```

Since

```text
Rainfall accumulation
=
Rainfall rate × Duration
```

and the duration is **0.5 hour**, multiplying by `0.5` converts the rainfall rate into accumulated rainfall for that half-hour period.

The backend then sums the rainfall from all downloaded granules:

```python
accumulation += rain_mm
```

The resulting raster represents the total rainfall accumulated during the requested 24-hour period.

## Building the Spatial Index

The IMERG rainfall grid consists of regularly spaced latitude and longitude coordinates.

The script first generates all grid-point coordinates:

```python
lon_grid, lat_grid = np.meshgrid(
    longitudes,
    latitudes,
)
```

The coordinate arrays are flattened into a list of longitude-latitude pairs:

```python
coords = np.column_stack((
    lon_grid.ravel(),
    lat_grid.ravel(),
))
```

A KD-tree is then created:

```python
tree = cKDTree(coords)
```

The KD-tree enables fast nearest-neighbour searches, which are used as a fallback when a footprint contains no IMERG grid points.

## Average Rainfall Computation

For each footprint:

1. Computes the polygon's bounding box.
2. Finds all IMERG grid points inside the bounding box.
3. Checks whether each candidate point lies inside the footprint.
4. Collects the rainfall values for those grid points.
5. Computes the arithmetic mean.
6. Stores the result as:

```javascript
feature.properties.gpmRainfall
```

Restricting the search to the bounding box significantly reduces the number of point-in-polygon tests compared to checking every IMERG grid point.

## Download Cache

Downloading 48 IMERG granules every time the dashboard refreshes would significantly increase response time.

To reduce unnecessary downloads, the backend maintains a cache organized by forecast time.

Example:

```text
backend/
└── data/
    └── gpm_cache/
        ├── 20260728_0200/
        │   ├── 3B-HHR-E.MS.MRG...
        │   ├── 3B-HHR-E.MS.MRG...
        │   └── ...
        └── 20260729_0200/
            └── ...
```

Whenever a forecast time is requested:

- If the corresponding cache already exists and contains all required granules, the cached files are reused.
- Otherwise, the missing IMERG granules are downloaded from NASA Earthdata.
- Old forecast caches are automatically removed so that only the latest forecast remains on disk.

This caching strategy substantially reduces dashboard loading time while minimizing repeated downloads from the Earthdata servers.

---

# Layer Controls

The dashboard includes a control panel that allows users to independently toggle:

- Synoptic Stations
- AWS Stations
- Footprints (Panahon)
- Footprints (ECMWF)
- Footprints (NASA GPM)

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

Clicking a Sentinel-1 satellite footprint displays:

- Sentinel-1 Satellite Footprint Tile Number
- Forecasted Date
- Sensing Time (Panahon)
- Sensing Time (ECMWF)
- Sensing Time (NASA GPM)
- Sampling Points Used
- Panahon API Forecast Rainfall (24 h)
- ECMWF Open Data Rainfall (24 h)
- NASA GPM IMERG Rainfall (24 h)

![Sentinel-1 Satellite Footprint Popup](/docs/footprint_popup.png)

> **Note**
>
> Sensing time from ECMWF is behind by 4 hours compared to the sensing time from Panahon to accommodate ECMWF's required time fields. Similarly, sensing time from NASA GPM is behind by 13 hours due to the fact that it's observational data based in UTC.

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
- Turf.js generated the initial sampling points, and point distribution is handled via Poisson disk sampling.
- Sampling points are reused between application runs.
- Forecast timestamps are generated dynamically; the forecast timestamp determines the visible Sentinel-1 satellite strip.
- Environment variables are accessed using `import.meta.env`.
- API tokens remain on the backend; `PANAHON_API_TOKEN` is read from the Django process environment.
- React focuses primarily on visualization.
- Available Panahon API data depends on initialization from `panahon.gov.ph`, which can occur in two cases:
  - Earliest rainfall accumulation hour starts from 8 PM the day before the initialization date. 
  - Earliest rainfall accumulation hour starts from 8 AM the day during the initialization date.
- Earthkit downloads ECMWF Open Data forecasts on demand.
- Earthaccess downloads NASA GPM IMERG Early Run (Half-Hourly files) observational data on demand.
- Earthaccess API requires an Earthdata account; credentials are saved as environment variables in backend.
- ECMWF and NASA GPM rainfall is calculated directly from raster cells instead of sampling discrete points.
- Sensing times for each model/API differ due to differences in timezone or specifications:
  - Panahon API data is synchronous with current Philippine time.
  - ECMWF Open Data is late by 4 hours from current Philippine time.
  - NASA GPM IMERG's earliest run is late by 13 hours from current Philippine time.
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

- Footprint rainfall endpoint
- Forecast datetime conversion service
- Earthkit dataset loader

NASA GPM

- Footprint rainfall endpoint
- Forecast datetime conversion service
- Earthdata login service
- Earthaccess dataset loader

Sentinel-1

- Forecast and initialization timestamp service
- Sentinel-1 satellite passes and strips service

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
- `footprintSamplePoints.json` and/or `footprintSamplePoints_C.json` contain valid coordinates
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
