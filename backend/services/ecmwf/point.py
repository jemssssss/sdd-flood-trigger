def get_ecmwf_point_value(*, url, t, lon, lat, init): 
    """ Temporary dummy ECMWF point sampler. 
        This is intentionally not connected to Panahon. 
        Later, replace this function with the real ECMWF point-sampling logic.
    """ 
    return { 
        "coordinates": [lon, lat], 
        "values": [3.9], 
    }