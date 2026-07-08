const BACKEND_BASE_URL = import.meta.env.VITE_BACKEND_BASE_URL || "http://localhost:8000";

export async function fetchEcmwfPoint({ 

    url = "prate_accum", 
    t,
    lon, 
    lat, 
    init,

}) { 

    const params = new URLSearchParams({ 
        url, 
        t, 
        lon: String(lon), 
        lat: String(lat), 
        init, 
    }); 

    const response = await fetch( `${BACKEND_BASE_URL}/ecmwf/point?${params.toString()}` ); 

    if (!response.ok) { 
        throw new Error(`ECMWF point request failed: ${response.status}`); 
    } 
    return response.json();

}