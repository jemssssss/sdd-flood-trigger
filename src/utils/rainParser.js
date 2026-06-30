export function parseRainStations(rawData) {
  const items = Array.isArray(rawData)
    ? rawData
    : rawData?.data || rawData?.results || [];

  return items
    .map((item, index) => {
      const latitude = Number(item.latitude ?? item.lat);
      const longitude = Number(item.longitude ?? item.lon ?? item.lng);
      const rainfallMm = Number(
        item.rain ?? item.rainfall ?? item.value ?? 0
      );

      if (!Number.isFinite(latitude) || !Number.isFinite(longitude)) {
        return null;
      }

      return {
        id:
          item.id ??
          item.site_id ??
          item.station_id ??
          `station-${index}`,

        stationName:
          item.stationName ??
          item.site_name ??
          item.station_name ??
          item.name ??
          "Unknown station",

        latitude,
        longitude,
        rainfallMm,

        observedAt:
          item.observedAt ??
          item.observed_at ??
          item.datetime ??
          item.timestamp ??
          null,

        raw: item,
      };
    })
    .filter(Boolean);
}