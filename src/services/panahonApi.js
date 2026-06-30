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