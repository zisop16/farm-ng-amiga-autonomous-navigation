import { Box, IconButton, List, ListItem, ListItemButton, ListItemText, Modal, Typography, TextField } from "@mui/material";
import DeleteIcon from '@mui/icons-material/Delete';
import EditIcon from '@mui/icons-material/Edit';
import CheckIcon from '@mui/icons-material/Check';

import React, { useEffect, useState } from "react";

const modalStyle = {
	position: 'absolute',
	top: '25%',
	left: '50%',
	transform: 'translate(-50%, -50%)',
	width: 600,
	bgcolor: 'background.paper',
	border: '2px solid #000',
	boxShadow: 24,
	p: 4,
};

interface TrackSelectProps {
	open: boolean,
	closeTrackSelect: VoidFunction,
	currentTrack: string,
	setTrack: (tName: string) => void
};

export default function TrackSelectModal(props: TrackSelectProps) {

	const [trackNames, setTrackNames] = useState([""]);
    const [editingTrack, setEditingTrack] = useState<string | null>(null);
    const [editedName, setEditedName] = useState("");
    const [error, setError] = useState(false);

	function fetchTrackNames(): void {
		setTrackNames(["track1", "track2"]);
	}

    function removeTrack(tName: string): void {
        setTrackNames(prevTrackNames => prevTrackNames.filter(track => track !== tName));

        if (tName === props.currentTrack) {
            props.setTrack("");
        }
    }
	
    function startEditing(tName:string): void {
        setEditingTrack(tName);
        setEditedName(tName);
        setError(false);
    }

    function saveTrackName(oldName: string): void {
        const trimmedName = editedName.trim();

        if (!trimmedName || (trimmedName !== oldName && trackNames.includes(trimmedName))) {
            setError(true);
            setEditedName(oldName);
            setTimeout(() => setEditingTrack(null), 2000);
            return;
        }

        setTrackNames(prevTrackNames =>
            prevTrackNames.map(track => (track === oldName ? trimmedName : track))
        );
        setEditingTrack(null);
        setError(false);
    }

	useEffect(fetchTrackNames, []);

	return (
		<>
			<Modal
				open={props.open}
				onClose={props.closeTrackSelect}
				aria-labelledby="track-modal-title"
				aria-describedby="track-modal-description"
			>
				<Box sx={modalStyle}>
					<Typography id="track-modal-title" variant="h4">
						Select a Track
					</Typography>
				<List id="track-modal-description">
					{ trackNames.map((tName: string) => {
						return <ListItem
							secondaryAction={
                                <>
                                {editingTrack === tName ? (
								    <IconButton edge="end" aria-label="rename" sx={{p: 1}} onClick={() => saveTrackName(tName)}>
									    <CheckIcon sx={{fontSize: 45}}/>
								    </IconButton>
                                ) : (
								    <IconButton edge="end" aria-label="rename" sx={{p: 1}} onClick={() => startEditing(tName)}>
									    <EditIcon sx={{fontSize: 45}}/>
								    </IconButton>
                                )}
								<IconButton edge="end" aria-label="delete" sx={{p: 1}} onClick={() => removeTrack(tName)}>
									<DeleteIcon sx={{fontSize: 45}}/>
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
                                    onBlur={() => saveTrackName(tName, true)}
                                    error={error}
                                    helperText={error ? "Track name already exists." : ""}
                                    autoFocus
                                    fullWidth
                                />
                            ) : (
							    <ListItemButton onClick={() =>props.setTrack(tName)}>
                                    <ListItemText primary={tName} />
                                </ListItemButton>
                            )}
                        </ListItem>
                    })}
                </List>
                </Box>
            </Modal>
        </>
    );
}
