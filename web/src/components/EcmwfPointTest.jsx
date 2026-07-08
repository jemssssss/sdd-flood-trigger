import { useState } from "react";
import { fetchEcmwfPoint } from "../services/ecmwfApi";

export default function EcmwfPointTest() { 
    const [loading, setLoading] = useState(false); 
    const [result, setResult] = useState(null); 
    const [error, setError] = useState(""); 
    
    async function handleTest() { 
        setLoading(true); 
        setError(""); 
        setResult(null); 
        
        try { 
            const data = await fetchEcmwfPoint({ 
                url: "prate_accum", 
                t: "2026-07-08T11:00:00", 
                lon: 126.34680273437502, 
                lat: 12.971578177493043, 
                init: "2026-07-07T12:00:00Z", 
            }); 
            
            setResult(data); 
        } catch (err) { 
            setError(err.message); 
        } finally { 
            setLoading(false); 
        } 
    } 
    
    return ( 
        <div className="panel"> 
            <h3>ECMWF Point Test</h3> 
            
            <button onClick={handleTest} disabled={loading}> 
                {loading ? "Loading..." : "Test ECMWF Point Endpoint"} 
            </button> 

            {error && <p className="error">{error}</p>}
            {result && ( 
                <pre>{JSON.stringify(result, null, 2)}</pre> 
            )} 
        </div> 
    );
}