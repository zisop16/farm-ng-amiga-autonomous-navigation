import { LinearProgress, Typography, TextField, Button, Grid2, Box } from "@mui/material";
import React, { useState } from "react";

interface TrackCreateProps {
    selectTrack: (trackName: string) => void,
    tracks: Array<string>,
    trackBeingCreated: boolean,
    setTrackBeingCreated: (setting: boolean) => void
};

enum TrackType {
    line,
    standard
};

export default function TrackCreateMenu(props: TrackCreateProps) {
    const [newTrackName, setNewTrackName] = useState("");
    const [trackType, setTrackType] = useState(TrackType.line);
    // This variable will store the error message associated with creating a given track
    const [trackCreationError, setTrackCreationError] = useState("");

    /*
    The add new track button should not add tracks directly into local storage;
    We have to make a call to backend API for the farmer to guide robot and create it, then it is added to backend and fetched
    */

    function createTrack() {
	    const trimmed = newTrackName.trim();
	    
	    if (trimmed === "") {
		    setTrackCreationError("Track name cannot be empty.");
		    return;
	    }
        if (trimmed.includes("\\") || trimmed.includes("/")) {
            setTrackCreationError("Track name cannot include the characters \\ or /");
            return;
        }
        console.log(props.tracks, trimmed);
	    if (props.tracks.includes(trimmed)) {
		    setTrackCreationError(`Track name: ${trimmed} already exists`);
		    return;
	    }

	    setTrackCreationError("");
	    props.setTrackBeingCreated(true);

	    // API call to start recording the track
        let record_url;
        if (trackType == TrackType.line) {
            record_url = `${import.meta.env.VITE_API_URL}/line/record/${trimmed}`;
        } else {
            record_url = `${import.meta.env.VITE_API_URL}/record/${trimmed}`;
        }
	    fetch(record_url, { method: "POST",})
	    .then(response => response.json())
	    .then(data => {
		    console.log(data.message);
	    });
	}

    function endTrackCreation() {
        // Make an API call to stop creating track object
        let stop_url;
        if (trackType == TrackType.line) {
            stop_url = `${import.meta.env.VITE_API_URL}/line/record/stop`;
        } else {
            stop_url = `${import.meta.env.VITE_API_URL}/record/stop`;
        }
        fetch(stop_url , {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            }
        })
        .then(response => response.json())
        .then(data => {
            console.log(data.message);
            props.setTrackBeingCreated(false);
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
                        disabled={props.trackBeingCreated}
                        error={trackCreationError !== ""}
                        helperText={trackCreationError}
                        style={{ width: "250px"}}
                    />
                </Grid2>
                <Grid2 size={12}>
                    <Button variant="contained" disabled={props.trackBeingCreated} onClick={createTrack} style={{ whiteSpace: "nowrap", minWidth: "120px" }}>
                        Start Track Creation
                    </Button>
                </Grid2>
                <Grid2 size={12}>
                    <Button variant="contained" disabled={!props.trackBeingCreated} onClick={endTrackCreation} style={{ whiteSpace: "nowrap", minWidth: "120px" }}>
                        End Track
                    </Button>
                </Grid2>
            </Grid2>
        </Box>
    );
}

