import { Box, IconButton, List, ListItem, ListItemButton, ListItemText, TextField, Button } from "@mui/material";
import DeleteIcon from '@mui/icons-material/Delete';
import EditIcon from '@mui/icons-material/Edit';
import CheckIcon from '@mui/icons-material/Check';

import React, { useEffect, useState } from "react";

const modalStyle = {
    bgcolor: 'background.paper',
    p: 4,
};

interface TrackSelectProps {
    currentTrack: string,
    setTrack: (tName: string) => void
};

export default function TrackSelectMenu(props: TrackSelectProps) {
    const [trackNames, setTrackNames] = useState<string[]>([""]);
    const [editingTrack, setEditingTrack] = useState<string | null>(null);
    const [editedName, setEditedName] = useState<string>("");
    const [error, setError] = useState(false);
    
    function fetchTrackNames(): void {
        const storedTrack = localStorage.getItem("trackNames");
        const trackArray = storedTrack ? JSON.parse(storedTrack) : null;

        if (!trackArray || trackArray.length === 0) {
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
        setError(false);
    }

    function saveTrackName(oldName: string): void {
        const trimmedName = editedName.trim();
        console.log("saveTrackName: trimmedName ...%s... oldName %s", trimmedName, oldName);

        if (!trimmedName || (trimmedName !== oldName && trackNames.includes(trimmedName))) {
            setError(true);
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
        console.log("saveTrackName: newTrackNames ...%s...", newTrackNames);
        setTrackNames(newTrackNames);
        console.log("saveTrackName: trackNames ...%s...", trackNames);
        localStorage.setItem('trackNames', JSON.stringify(newTrackNames));

        if (props.currentTrack === oldName) {
            props.setTrack(trimmedName);
        }

        setEditingTrack(null);
        setError(false);
    }

    useEffect(fetchTrackNames, []);

    return (
        <Box sx={modalStyle}>
            <List id="track-modal-description">
                {trackNames.map((tName: string) => {
                    return (
                        <ListItem
                            secondaryAction={
                                <>
                                    {editingTrack === tName ? (
                                        <IconButton edge="end" aria-label="rename" sx={{ p: 1 }} onClick={() => saveTrackName(tName)}>
                                            <CheckIcon sx={{ fontSize: 45 }} />
                                        </IconButton>
                                    ) : (
                                        <IconButton edge="end" aria-label="rename" sx={{ p: 1 }} onClick={() => startEditing(tName)}>
                                            <EditIcon sx={{ fontSize: 45 }} />
                                        </IconButton>
                                    )}
                                    <IconButton edge="end" aria-label="delete" sx={{ p: 1 }} onClick={() => removeTrack(tName)}>
                                        <DeleteIcon sx={{ fontSize: 45 }} />
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
                                        setError(false);
                                    }}
                                    onKeyDown={(e) => e.key === "Enter" && saveTrackName(tName)}
                                    onBlur={() => saveTrackName(tName)}
                                    error={error}
                                    helperText={error ? `Track name: ${editingTrack} already exists.` : ""}
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

