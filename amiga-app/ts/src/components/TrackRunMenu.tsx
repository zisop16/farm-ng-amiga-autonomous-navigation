import { LinearProgress, Typography, TextField, Button, Grid2, Box } from "@mui/material";
import React, { useEffect, useState } from "react";
import { Vec2, FromPolar, twoDigits } from "../utils/Vec2";
import Arrow from '@elsdoerfer/react-arrow';

interface TrackRunProps {
    selectedTrack: string
};

export default function TrackRunMenu(props: TrackRunProps) {
    const boxStyle = {
        bgcolor: "#cce7eb",
        p: 4,
        margin: "20px 0 0 0",
        boxShadow: 24,
    };
    const API_URL = "http://localhost:8042";

    const [currentLocation, setCurrentLocation] = useState(Vec2.Zero);
    const [startPosition, setStartPosition] = useState(Vec2.Zero);
    const [rotationAngle, updateRotationAngle] = useState(0);

    useEffect(() => {
        const detailSocket = new WebSocket(
            `${API_URL}/filter_data`
        );

        detailSocket.onopen = (event) => {
            console.log('Detail WebSocket connection opened:', event);
        };

        detailSocket.onmessage = (event) => {
            const transform = JSON.parse(JSON.parse(event.data))["pose"]["aFromB"];
            const translation = transform["translation"];
            setCurrentLocation(new Vec2(translation.x, translation.y));
            const zAxisRotation = Math.acos(transform["rotation"]["unitQuaternion"]["real"]) * 2;
            updateRotationAngle(zAxisRotation);
            // console.log(zAxisRotation);
        }

        detailSocket.onclose = (event) => {
            console.log('Detail WebSocket connection closed:', event);
        };
        // This websocket will never close
        // Oh well.
        // return () => {detailSocket.close()};
    }, []);

    

    function fetchStartingPoint() {
        const trackDataEndpoint = `${API_URL}/get_track/${props.selectedTrack}`;
        fetch(trackDataEndpoint, { method: "GET" })
        .then((response) => response.json())
        .then((result) => {
            const waypoints = result["waypoints"];
            const first = waypoints[0];
            const startingPos = first["aFromB"]["translation"]
            setStartPosition(new Vec2(startingPos.x, startingPos.y));
        })
        .catch((err) => console.log(err));
    }

    function getDist() {
        const diff: Vec2 = currentLocation.Sub(startPosition);
        return diff.Mag();
    }

    // Returns the angle in radians between the robot's current rotation
    // and the angle it needs to rotate in order to be facing a straight line towards
    // the starting position
    function rotationTarget() {
        const diff = startPosition.Sub(currentLocation);
        const targetAngleVec = diff.Normalized();
        const currentAngleVec = FromPolar(1, rotationAngle);
        const currAngle = currentAngleVec.Argument();
        const targetAngle = targetAngleVec.Argument();
        console.log(currAngle, targetAngle);
        return (-targetAngle + currAngle) * 180/Math.PI;
    }

    useEffect(fetchStartingPoint, [props.selectedTrack]);
    return (
    <Box sx={boxStyle}>
        <Grid2 container rowSpacing={2} style={{display: "flex", alignItems: "center", gap: "10px"}}>
            <Grid2 size={12}>
                <Typography variant="h6">Distance: {twoDigits(getDist())}</Typography>
            </Grid2>
            <Grid2 size={12} style={{justifyContent: "center", display: "flex"}}>
                <Typography variant="h6">
                    <b><u>Direction</u></b>
                </Typography>
            </Grid2>
            <Grid2 size={12} style={{justifyContent: "center", display: "flex"}}>
                <Arrow 
                angle={rotationTarget()}
                length={100}
                lineWidth={10}
                style={{
                    width: "100px",
                    height: "100px"
                }}
                />
            </Grid2>
        </Grid2>
    </Box>
    );
}