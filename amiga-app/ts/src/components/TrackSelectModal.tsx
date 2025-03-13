import { Box, IconButton, List, ListItem, ListItemButton, ListItemText, Modal, Typography } from "@mui/material";
import DeleteIcon from '@mui/icons-material/Delete';

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
	currentTrack: string
	setTrack: (tName: string) => void
};

export default function TrackSelectModal(props: TrackSelectProps) {

	const [trackNames, setTrackNames] = useState([""]);

	function fetchTrackNames(): void {
		setTrackNames(["track1", "track2"]);
	}

	function removeTrack(tName: string): void {
		let trackInd = trackNames.indexOf(tName);
		let newTrackNames = trackNames;
		delete newTrackNames[trackInd];
		setTrackNames(newTrackNames);
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
								<IconButton edge="end" aria-label="delete" sx={{p: 1}} onClick={() => removeTrack(tName)}>
									<DeleteIcon sx={{fontSize: 45}}/>
								</IconButton>
							}
							disablePadding
						>
							<ListItemButton onClick={() => props.setTrack(tName)}>
								<ListItemText primary={tName}/>
							</ListItemButton>
						</ListItem>
						})
					}
				</List>
				</Box>
			</Modal>
		</>
	);
}
