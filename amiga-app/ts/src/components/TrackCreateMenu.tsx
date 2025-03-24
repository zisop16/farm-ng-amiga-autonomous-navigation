import { LinearProgress, Typography, TextField, Button, Grid2, Box } from "@mui/material";
import React, { useState } from "react";

interface TrackCreateProps {
    setTrack: (trackName: string) => void,
};

export default function TrackCreateMenu(props: TrackCreateProps) {
    const [newTrackName, setNewTrackName] = useState("");
    // This variable will store the track name entered which caused duplicate error
    const [duplicateTrackError, setDuplicateTrackError] = useState("");
    const [currentlyCreating, setCurrentlyCreating] = useState(false)

    /*
    The add new track button should not add tracks directly into local storage;
    We have to make a call to backend API for the farmer to guide robot and create it, then it is added to backend and fetched
    */

    function getTrackErrorMessage() {
   	    return duplicateTrackError ? `Track name "${duplicateTrackError}" already exists.` : "";
    }

    function createTrack() {
	    const trimmed = newTrackName.trim();
	    
	    if (!trimmed) {
		setDuplicateTrackError("Track name cannot be empty.");
		return;
	    }

	    const toParse = localStorage.getItem("trackNames");
	    const trackNames = toParse ? JSON.parse(toParse) : [];

	    if (trackNames.includes(trimmed)) {
		setDuplicateTrackError(trimmed);
		return;
	    }

	    setDuplicateTrackError("");
	    setCurrentlyCreating(true);

	    // API call to start recording the track
        const recording = `${import.meta.env.VITE_API_URL}/record/${encodeURIComponent(trimmed)}`;
	    fetch(recording, {
		method: "POST",
		headers: {
		    "Content-Type": "application/json",
		},
	    })
	    .then(response => response.json())
	    .then(data => {
		console.log(data.message);
	    })
	    .catch(error => {
		console.error("Error starting track recording:", error);
		setCurrentlyCreating(false); // Ensure state is reverted on failure
	    });
	}

    function endTrackCreation() {
        // Make an API call to stop creating track object
        const stopping = `${import.meta.env.VITE_API_URL}/stop_recording`;
        fetch(stopping , {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error("Failed to stop recording");
            }
            return response.json();
        })
        .then(data => {
            console.log(data.message);
            setCurrentlyCreating(false);
        })
        .catch(error => {
            console.error("Error stopping recording:", error);
        });
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

