import { Grid2, LinearProgress, Typography } from "@mui/material";
import React from "react";

export default function TrackCreateMenu() {
	return (
		<Grid2 container rowSpacing={2} style={{ margin: "30px 30px 0 30px" }}>
			<Grid2 size="auto">
				<Typography variant="h5">Track Progress:</Typography>
			</Grid2>
			<Grid2 size={.3} />
			<Grid2 size="grow">
				<LinearProgress variant="determinate" value={50} sx={{backgroundColor: 'pink', height: 30}}/>
			</ Grid2>
		</ Grid2>
	);
}