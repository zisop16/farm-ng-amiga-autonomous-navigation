import { Box, IconButton, List, ListItem, ListItemButton, ListItemText, TextField, Button, Typography } from "@mui/material";
import DeleteIcon from '@mui/icons-material/Delete';
import EditIcon from '@mui/icons-material/Edit';
import CheckIcon from '@mui/icons-material/Check';

import React, { useEffect, useState } from "react";

interface TrackSelectProps {
    selectedTrack: string,
    selectTrack: (tName: string) => void,
    tracks: Array<string>,
    editTracks: (newTracks: Array<string>) => void,
};


export default function TrackSelectMenu(props: TrackSelectProps) {
    const [editingTrack, setEditingTrack] = useState<string | null>(null);
    const [editedName, setEditedName] = useState<string>("");
    // The string should be equal to the name which was duplicated, whenever this error is active
    const [duplicateNameError, setDuplicateNameError] = useState("");

    function removeTrack(tName: string): void {
        const delete_url = `${import.meta.env.VITE_API_URL}/delete_track/${tName}`;
	    fetch(delete_url, {
            method: "POST",
	    })
	    .then(response => {
            return response.json();
	    })
	    .then(data => {
		    console.log(data.message);
		    props.editTracks(props.tracks.filter(track => track !== tName));

            if (tName === props.selectedTrack) {
                props.selectTrack("");
            }
	    });
	}

    function startEditing(tName: string): void {
        setEditingTrack(tName);
        setEditedName(tName);
        setDuplicateNameError("");
    }

    ///////////
    function saveTrackName(oldName: string): void {
        const trimmedName = editedName.trim();
    
        if (!trimmedName || (trimmedName !== oldName && props.tracks.includes(trimmedName))) {
            setDuplicateNameError(trimmedName);
            setEditedName(oldName);
            return;
        }
    
        const newTrackNames = props.tracks.map((t) => {
            if (t === oldName) {
                return trimmedName;
            } else {
                return t;
            }
        });
    
        // Make API call to rename track
        fetch(`${import.meta.env.VITE_API_URL}/edit_track`, {
            method: "POST",
            body: JSON.stringify({
                current_name: oldName,  // Proper JSON structure for the Pydantic model
                new_name: trimmedName
            })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`Failed to rename track: ${response.statusText}`);
            }
            return response.json();
        })
        .then(data => {
            console.log("Track renamed successfully:", data.message);
            props.editTracks(newTrackNames);
    
            if (props.selectedTrack === oldName) {
                props.selectTrack(trimmedName);
            }
    
            setEditingTrack(null);
            setDuplicateNameError("");
        })
        .catch(error => {
            console.error("Error renaming track:", error);
        });
    }
    
    
///////////
    const iconStyle = {
        fontSize: 45
    };

    const boxStyle = {
        bgcolor: "#cce7eb",
        p: 4,
        margin: "20px 0 0 0",
        boxShadow: 24,
    };

    return (
        <Box sx={boxStyle}>
            <Typography variant="h4">
                Available Tracks:
            </Typography>
            <List id="track-modal-description">
                {props.tracks.map((tName: string) => {
                    return (
                        <ListItem
                            key={tName}
                            secondaryAction={
                                <>
                                    {editingTrack === tName ? (
                                        <IconButton edge="end" aria-label="rename" sx={{ p: 1 }} onClick={() => saveTrackName(tName)}>
                                            <CheckIcon sx={iconStyle} />
                                        </IconButton>
                                    ) : (
                                        <IconButton edge="end" aria-label="rename" sx={{ p: 1 }} onClick={() => startEditing(tName)}>
                                            <EditIcon sx={iconStyle} />
                                        </IconButton>
                                    )}
                                    <IconButton edge="end" aria-label="delete" sx={{ p: 1 }} onClick={() => removeTrack(tName)}>
                                        <DeleteIcon sx={iconStyle} />
                                    </IconButton>
                                </>
                            }
                            disablePadding
                        >
                            {editingTrack === tName ? (
                                <TextField
                                    value={editedName}
                                    onChange={(e) => {
                                        setEditedName(e.target.value);
                                        setDuplicateNameError("");
                                    }}
                                    onKeyDown={
                                        (event) => {
                                            if (event.key === "Enter") {
                                                saveTrackName(tName);
                                            }
                                        }
                                    }
                                    onBlur={() => saveTrackName(tName)}
                                    error={duplicateNameError !== ""}
                                    helperText={duplicateNameError ? `Track name: ${duplicateNameError} already exists.` : ""}
                                    autoFocus
                                    fullWidth
                                />
                            ) : (
                                <ListItemButton onClick={() => props.selectTrack(tName)}>
                                    <ListItemText primary={tName} />
                                </ListItemButton>
                            )}
                        </ListItem>
                    );
                })}
            </List>
        </Box>
    );
}

