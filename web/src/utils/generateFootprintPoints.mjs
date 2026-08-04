import fs from "fs";
import * as turf from "@turf/turf";
import PoissonDiskSampling from "poisson-disk-sampling";

const SAMPLE_POINTS = Number(
  process.env.VITE_SAMPLING_POINTS ?? 25
);

const geojson = JSON.parse(
  fs.readFileSync(
    "./public/data/s1a_footprints.geojson",
    "utf8"
  )
);

const output = [];

for (const feature of geojson.features) {

  const bbox = turf.bbox(feature);

  const minLon = bbox[0];
  const minLat = bbox[1];
  const maxLon = bbox[2];
  const maxLat = bbox[3];

  const width = maxLon - minLon;
  const height = maxLat - minLat;

  // Estimate a minimum spacing that will produce roughly SAMPLE_POINTS.

  const area = width * height;
  const minDistance = Math.sqrt(area / SAMPLE_POINTS) * 0.75;

  const sampler = new PoissonDiskSampling({
    shape: [width, height],
    minDistance,
    maxDistance: minDistance * 1.5,
    tries: 30
  });

  const candidates = sampler.fill();
  const accepted = [];
  for (const candidate of candidates) {
    const lon = candidate[0] + minLon;
    const lat = candidate[1] + minLat;

    const point = turf.point([lon, lat]);
    if (
      turf.booleanPointInPolygon(
        point,
        feature
      )
    ) {
      accepted.push({
        lat,
        lon,
      });
    }

  }

  // If we generated too many, randomly keep SAMPLE_POINTS.

  if (accepted.length > SAMPLE_POINTS) {
    accepted.sort(
      () => Math.random() - 0.5
    );

    accepted.length = SAMPLE_POINTS;
  }

  /*
    If too few remain (possible for thin
    polygons), keep generating using a
    smaller spacing.
  */

  let distance = minDistance;

  while (
    accepted.length < SAMPLE_POINTS
  ) {

    distance *= 0.9;
    const retry = new PoissonDiskSampling({
      shape: [width, height],
      minDistance: distance,
      maxDistance: distance * 1.5,
      tries: 30
    });

    const retryCandidates = retry.fill();
    for (const candidate of retryCandidates) {
      if (
        accepted.length >= SAMPLE_POINTS
      ) {
        break;
      }

      const lon = candidate[0] + minLon;
      const lat = candidate[1] + minLat;

      const point = turf.point([
        lon,
        lat,
      ]);

      if (
        !turf.booleanPointInPolygon(
          point,
          feature
        )
      ) {
        continue;
      }

      // Avoid duplicates.

      let duplicate = false;
      for (const existing of accepted) {
        const dx = existing.lon - lon;

        const dy = existing.lat - lat;

        if (
          Math.sqrt(
            dx * dx + dy * dy
          ) < distance * 0.5
        ) {

          duplicate = true;
          break;

        }

      }

      if (!duplicate) {
        accepted.push({
          lat,
          lon,
        });

      }

    }

  }

  output.push({
    tile: feature.properties.TileNumber,
    samplePoints: accepted,
  });

}

fs.writeFileSync(
  "./public/data/footprintSamplePoints.json",
  JSON.stringify(
    output,
    null,
    2
  )

);

console.log(
  `Generated ${SAMPLE_POINTS} Poisson-distributed sample points per footprint.`
);