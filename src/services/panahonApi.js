export async function fetchRainSynop() {
	const token = import.meta.env.VITE_PANAHON_API_TOKEN;

	if (!token) {
		throw new Error("Missing VITE_PANAHON_API_TOKEN");
	}

	const url =
		`https://www.panahon.gov.ph/api/v1/synop?token=${token}&parameter=rain`;

	const response = await fetch(url);

	if (!response.ok) {
		throw new Error(
			`Panahon API request failed: ${response.status}`
		);
	}

	return response.json();
}

export async function fetchPointRainfall(lat, lon, time) {
  const token = import.meta.env.VITE_PANAHON_API_TOKEN;

  if (!token) {
    throw new Error("Missing VITE_PANAHON_API_TOKEN");
  }

  const url =
    `https://www.panahon.gov.ph/api/v1/tiles/point` +
    `?url=prate` +
    `&lat=${lat}` +
    `&lon=${lon}` +
    `&t=${encodeURIComponent(time)}` +
    `&token=${token}`;

  const response = await fetch(url);

  if (!response.ok) {
    throw new Error(`Point rainfall request failed: ${response.status}`);
  }

  const data = await response.json();

  return data.values?.[0] ?? 0;
}