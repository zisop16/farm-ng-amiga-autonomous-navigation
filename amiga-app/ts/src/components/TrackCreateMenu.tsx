/* eslint-disable @typescript-eslint/no-unused-vars */
import { Grid, LinearProgress, Typography, TextField, Button, Grid2, Box } from "@mui/material";
import React, { useState } from "react";

interface CameraFeedProps {
    setTrack: (trackName: string) => void,
};

export default function TrackCreateMenu(props: CameraFeedProps) {
    const [newTrackName, setNewTrackName] = useState("");
    // This variable will store the track name entered which caused duplicate error
    const [duplicateTrackError, setDuplicateTrackError] = useState("");
    const [currentlyCreating, setCurrentlyCreating] = useState(false)

    /*
    The add new track button should not add tracks directly into local storage;
    We have to make a call to backend API for the farmer to guide robot and create it, then it is added to backend and fetched
    */
    function createTrack() {
        const trimmed = newTrackName.trim();
        // Make typescript stop complaining about possibility of null
        const toParse: string | null = localStorage.getItem("trackNames")
        if (toParse === null) {return;}
        const trackNames: Array<string> = JSON.parse(toParse);

        if (trackNames.includes(trimmed)) {
            setDuplicateTrackError(trimmed);
            return;
        }
        // No duplicate track error
        setDuplicateTrackError("");
        setCurrentlyCreating(true);

        // Make an API call to start creating track object
    }

    function endTrackCreation() {
        // Make an API call to stop creating track object
        setCurrentlyCreating(false);
    }

    function getTrackErrorMessage(): string {
        if (duplicateTrackError === "") {
            return "";
        }
        return `Track name: ${duplicateTrackError} already exists`;
    }

    const boxStyle = {
        bgcolor: "#cce7eb",
        p: 4,
        margin: "20px 0 0 0",
        boxShadow: 24,
    };

    return (
        <Box sx={boxStyle}>
            <Grid2 container rowSpacing={2} style={{display: "flex", alignItems: "center", gap: "10px"}}>
                <Grid2 size={12}>
                    <TextField
                        label="Track Name: "
                        value={newTrackName}
                        onChange={(e) => setNewTrackName(e.target.value)}
                        placeholder="Enter new track name"
                        disabled={currentlyCreating}
                        error={duplicateTrackError !== ""}
                        helperText={getTrackErrorMessage()}
                        style={{ width: "250px"}}
                    />
                </Grid2>
                <Grid2 size={12}>
                    <Button variant="contained" disabled={currentlyCreating} onClick={createTrack} style={{ whiteSpace: "nowrap", minWidth: "120px" }}>
                        Start Track Creation
                    </Button>
                </Grid2>
                <Grid2 size={12}>
                    <Button variant="contained" disabled={!currentlyCreating} onClick={endTrackCreation} style={{ whiteSpace: "nowrap", minWidth: "120px" }}>
                        End Track
                    </Button>
                </Grid2>
            </Grid2>
        </Box>
    );
}

