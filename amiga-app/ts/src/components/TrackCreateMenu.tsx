import { Grid, LinearProgress, Typography, TextField, Button } from "@mui/material";
import React, { useState } from "react";

export default function TrackCreateMenu({ setTrack }) {
    const [newTrackName, setNewTrackName] = useState("");
    const [error, setError] = useState(false);

    function addNewTrack() {
        const trimmedTrackName = newTrackName.trim();
        if (trimmedTrackName && localStorage.getItem("trackNames") && JSON.parse(localStorage.getItem("trackNames")).includes(trimmedTrackName)) {
            setError(true);
        } else if (trimmedTrackName) {
            const updatedTracks = [...JSON.parse(localStorage.getItem("trackNames") || '[]'), trimmedTrackName];
            localStorage.setItem('trackNames', JSON.stringify(updatedTracks));
            setTrack(trimmedTrackName);
            setNewTrackName('');
            setError(false);
        }
    }

    return (
        <Grid container rowSpacing={2} style={{ margin: "30px 30px 0 30px" }}>
            <Grid item xs={12}>
                <Typography variant="h5">Track Progress:</Typography>
            </Grid>
            <Grid item xs={12}>
                <LinearProgress variant="determinate" value={50} sx={{ backgroundColor: 'pink', height: 30 }} />
            </Grid>

            <Grid item xs={12} style={{ marginTop: "80px", display: "flex", alignItems: "center", gap: "10px" }}>
                <TextField
                    value={newTrackName}
                    onChange={(e) => setNewTrackName(e.target.value)}
                    onBlur={addNewTrack}
                    onKeyDown={(e) => e.key === "Enter" && addNewTrack()}
                    placeholder="Enter new track name"
                    error={error}
                    helperText={error ? "Track name already exists" : ""}
                    style={{ width: "250px" }}
                />
                <Button variant="contained" onClick={addNewTrack} style={{ whiteSpace: "nowrap", minWidth: "120px" }}>
                    Add Track
                </Button>
            </Grid>
        </Grid>
    );
}

