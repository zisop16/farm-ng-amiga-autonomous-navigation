import { Button, Grid2, LinearProgress, Stack, Tab, Tabs, Typography } from "@mui/material";
import BackButton from "../components/BackButton";
import CameraFeed from "../components/CameraFeed";
import React, { useEffect } from "react";
import TrackSelectModal from "../components/TrackSelectModal";
import { useNavigate } from "react-router";

export default function TrackSelect() {
    const [tabValue, setTabValue] = React.useState(1);
    const [currentCamera, setCurrentCamera] = React.useState("center");
    const [trackName, setTrackName] = React.useState("");

    const [trackSelectOpen, setTrackSelectOpen] = React.useState(false);

    const openTrackSelect = () => setTrackSelectOpen(true);
    const closeTrackSelect = () => setTrackSelectOpen(false);
    const setTrack = (tName: string) => setTrackName(tName);

    const navigate = useNavigate();

    useEffect(() => {
            const storedTrack = localStorage.getItem("trackName");
            if (storedTrack !== null) {
                const asStr = JSON.parse(storedTrack);
                if (asStr !== "") {
                    setTrackName(asStr);
                }
            }
        }, []);

    useEffect(() => {
        localStorage.setItem('trackName', JSON.stringify(trackName));
      }, [trackName]
    );

    function runTrack() {

    }

    const handleCameraTabChange = (event: React.SyntheticEvent, newValue: number) => {
        setTabValue(newValue);
        setCurrentCamera(event.currentTarget.id);
    };

    const buttonStyle = {
        width: "500px",
        height: "130px",
        borderRadius: "4px"
    };

    return (
        <>
            <TrackSelectModal open={trackSelectOpen} closeTrackSelect={closeTrackSelect} currentTrack={trackName} setTrack={setTrack}/>
            <Grid2 container rowSpacing={2} style={{ margin: "30px 0 0 30px" }} >
                <Grid2 size={1} display="flex" justifyContent="center" alignItems="center">
                    <BackButton />
                </Grid2>
                <Grid2 size={10} display="flex" justifyContent="center" alignItems="center">
                    <Typography variant="h2">Track Select</Typography>
                </Grid2>
                <Grid2 size="grow" />

                <Grid2 size={12}>
                    <div style={{ width: "640px" }}>
                        <Tabs value={tabValue} onChange={handleCameraTabChange} variant="fullWidth">
                            <Tab label=<Typography>Left Camera</Typography> id="left" />
                            <Tab label=<Typography>Center Camera</Typography> id="center" />
                            <Tab label=<Typography>Right Camera</Typography> id="right" />
                        </Tabs>
                    </div>
                </Grid2>

                <CameraFeed orientation={currentCamera} />

                <Grid2 size={.3} />

                <Grid2 size="auto">
                    <Stack rowGap={1} spacing="auto" sx={{ flexGrow: 1, justifyContent: 'space-between', height: '100%' }}>
                        <Button variant="contained" style={buttonStyle} onClick={() => navigate("/TrackCreate")}>
                            <Typography variant="h5">Add New Track</Typography>

                        </Button>
                        <Button variant="contained" style={buttonStyle} onClick={runTrack}>
                            <Typography variant="h5">Run Track</Typography>
                        </Button>
                        <Button variant="contained" style={buttonStyle} onClick={openTrackSelect}>
                            <Typography variant="h5">View Tracks</Typography>
                        </Button>
                    </Stack>
                </Grid2>

                <Grid2 size="grow" />
                <Grid2 size={0} />

                <Grid2 size="auto">
                    <Typography variant="h5">Track Progress:</Typography>
                </Grid2>
                <Grid2 size={.3} />
                <Grid2 size="grow">
                    <LinearProgress variant="determinate" value={50} sx={{backgroundColor: 'pink', height: 30}}/>
                </Grid2>
                <Grid2 size={4}/>
                <Grid2 size={12}>
                    <Typography variant="h5">
                        Current Track: {
                            trackName == "" ? "None" : trackName
                        }
                    </Typography>
                </Grid2>

            </Grid2>
        </>
    )
}
