import { Box, IconButton, List, ListItem, ListItemButton, ListItemText, TextField, Button, Typography } from "@mui/material";
import DeleteIcon from '@mui/icons-material/Delete';
import EditIcon from '@mui/icons-material/Edit';
import CheckIcon from '@mui/icons-material/Check';

import React, { useEffect, useState } from "react";

interface TrackSelectProps {
    currentTrack: string,
    setTrack: (tName: string) => void
};

export default function TrackSelectMenu(props: TrackSelectProps) {
    const [trackNames, setTrackNames] = useState<string[]>([""]);
    const [editingTrack, setEditingTrack] = useState<string | null>(null);
    const [editedName, setEditedName] = useState<string>("");
    // The string should be equal to the name which was duplicated, whenever this error is active
    const [duplicateNameError, setDuplicateNameError] = useState("");
    
    function fetchTrackNames(): void {
        const storedTrack = localStorage.getItem("trackNames");
        const trackArray = storedTrack ? JSON.parse(storedTrack) : null;

        if (trackArray === null || trackArray.length === 0) {
            setTrackNames(["track1", "track2"]);
            localStorage.setItem("trackNames", JSON.stringify(["track1", "track2"]));
        } else {
            setTrackNames(trackArray);
        }
    }

    function removeTrack(tName: string): void {
        setTrackNames(prevTrackNames => {
            const updatedTracks = prevTrackNames.filter(track => track !== tName);
            localStorage.setItem("trackNames", JSON.stringify(updatedTracks)); 
            return updatedTracks;
        });

        if (tName === props.currentTrack) {
            props.setTrack("");
        }
    }

    function startEditing(tName: string): void {
        setEditingTrack(tName);
        setEditedName(tName);
        setDuplicateNameError("");
    }

    function saveTrackName(oldName: string): void {
        const trimmedName = editedName.trim();

        if (!trimmedName || (trimmedName !== oldName && trackNames.includes(trimmedName))) {
            setDuplicateNameError(trimmedName);
            setEditedName(oldName);
            return;
        }

        const newTrackNames = trackNames.map((t, i) => {
            if (t === oldName) {
                return trimmedName;
            } else {
                return t;
            }
        });

        setTrackNames(newTrackNames);
        localStorage.setItem('trackNames', JSON.stringify(newTrackNames));

        if (props.currentTrack === oldName) {
            props.setTrack(trimmedName);
        }

        setEditingTrack(null);
        setDuplicateNameError("");
    }

    useEffect(fetchTrackNames, []);

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
                {trackNames.map((tName: string) => {
                    return (
                        <ListItem
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
                                <ListItemButton onClick={() => props.setTrack(tName)}>
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

