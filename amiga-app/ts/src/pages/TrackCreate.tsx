import { Button, Grid2, Typography } from "@mui/material";
import React, { useEffect, useState } from "react";
import BackButton from "../components/BackButton";

export default function TrackCreate() {
    const [foundTrack, setFoundTrack] = useState(false);
    const [trackName, setTrackName] = useState("");
    const [collectingWaypoints, setCollectingWayPoints] = useState(false);

    useEffect(() => {
        const storedTrack = localStorage.getItem("trackName");
        if (storedTrack === null) {
            setFoundTrack(false);
        } else {
            const asStr = JSON.parse(storedTrack);
            if (asStr === "") {
                setFoundTrack(false);
            } else {
                setTrackName(asStr);
                setFoundTrack(true);
            }
        }
    }, []);

    function changeCollecting() {
        if (collectingWaypoints) {
            // Tell robot to stop collecting
        } else {
            // Tell robot to start collecting
        }
        setCollectingWayPoints(!collectingWaypoints);
    }

    const buttonStyle = {
        width: "500px",
        height: "130px",
        borderRadius: "4px"
    };

    return (
        <>
            <Grid2 container rowSpacing={2} style={{ margin: "30px 0 0 30px" }} >
                <Grid2 size={1} display="flex" justifyContent="center" alignItems="center">
                    <BackButton />
                </Grid2>
                
                <Grid2 size={10} display="flex" justifyContent="center" alignItems="center">
                    <Typography variant="h4">Creating Track: {foundTrack ? trackName : "No Track Found"}</Typography>
                </Grid2>

                <Grid2 size={1} />

                <Grid2 size={12} display="flex" justifyContent="center" alignItems="center">
                    <Button variant="contained" style={buttonStyle} onClick={changeCollecting}>
                        <Typography variant="h5">{collectingWaypoints ? "Stop" : "Start"} Collecting Waypoints</Typography>
                    </Button>
                </Grid2>
                
            </Grid2>
        </>
    );
}