import "../styles/App.css";

function LayerControl({

	showSynoptic,
	setShowSynoptic,

	showAWS,
	setShowAWS,

	showPanahonFootprints,
	setShowPanahonFootprints,

	showEcmwfFootprints,
	setShowEcmwfFootprints,

}) {

	return (

		<div className="layer-control">

				<h3>Layers</h3>

				<label>

					<input
						type="checkbox"
						checked={showSynoptic}
						onChange={(e)=>
							setShowSynoptic(e.target.checked)
						}
					/>

					Synoptic Stations

				</label>

				<label>

					<input
						type="checkbox"
						checked={showAWS}
						onChange={(e)=>
							setShowAWS(e.target.checked)
						}
					/>

					AWS Stations

				</label>

				<label>

					<input
						type="checkbox"
						checked={showPanahonFootprints}
						onChange={(e)=>
							setShowPanahonFootprints(e.target.checked)
						}
					/>

					Footprints (Panahon)

				</label>

				<label>

					<input
						type="checkbox"
						checked={showEcmwfFootprints}
						onChange={(e)=>
							setShowEcmwfFootprints(e.target.checked)
						}
					/>

					Footprints (ECMWF)

				</label>

		</div>

	);

}

export default LayerControl;