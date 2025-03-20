import { LinearProgress, Typography, TextField, Button, Grid2, Box } from "@mui/material";
import React, { useEffect, useState } from "react";

interface TrackRunProps {
    selectedTrack: string,
};

export default function TrackRunMenu(props: TrackRunProps) {
    const boxStyle = {
        bgcolor: "#cce7eb",
        p: 4,
        margin: "20px 0 0 0",
        boxShadow: 24,
    };
    function fetchStartingPoint() {

    }
    function fetchCurrentLocation() {
        
    }
    useEffect(fetchStartingPoint, [props.selectedTrack]);
    return (
    <Box sx={boxStyle}>
        <Grid2 container rowSpacing={2} style={{display: "flex", alignItems: "center", gap: "10px"}}>
            <Typography variant="h6">Distance from starting point:</Typography>
        </Grid2>
    </Box>
    );
}