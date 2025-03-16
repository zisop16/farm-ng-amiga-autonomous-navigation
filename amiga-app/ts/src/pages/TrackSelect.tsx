import { Button, Collapse, Container, Grid2, LinearProgress, Stack, Tab, Tabs, Typography } from "@mui/material";
import BackButton from "../components/BackButton";
import CameraFeed from "../components/CameraFeed";
import React, { useEffect } from "react";
import TrackSelectMenu from "../components/TrackSelectMenu";
import TrackCreateMenu from "../components/TrackCreateMenu";

export default function TrackSelect() {
    const [tabValue, setTabValue] = React.useState(1);
    const [currentCamera, setCurrentCamera] = React.useState("center");
    const [trackName, setTrackName] = React.useState("");
    const [selectedButton, changeSelectedButton] = React.useState("select");

    const setTrack = (tName: string) => setTrackName(tName);

    useEffect(() => {
            const storedTrack = localStorage.getItem("trackName");
            if (storedTrack !== null) {
                setTrackName(JSON.parse(storedTrack));
            }
        }, []);

    function getMenuComponent() {
        switch(selectedButton) {
            case "add":
                return <TrackCreateMenu setTrack={setTrack} />;
            case "select":
                return (<TrackSelectMenu currentTrack={trackName} setTrack={setTrack}/>);
            case "run":
                return <> </>;
            default:
                return (<></>);
        }
    }

    const handleCameraTabChange = (event: React.SyntheticEvent, newValue: number) => {
        setTabValue(newValue);
        setCurrentCamera(event.currentTarget.id);
    };

    const buttonStyle = {
        width: "150px",
        height: "130px",
        borderRadius: "4px"
    };

    return (
        <>
            <Grid2 container rowSpacing={2} style={{ margin: "30px 30px 0 30px" }} >
                <Grid2 size={1} display="flex" justifyContent="center" alignItems="center">
                    <BackButton />
                </Grid2>
                <Grid2 size={10} display="flex" justifyContent="center" alignItems="center">
                    <Typography variant="h2">Track Select</Typography>
                </Grid2>
                <Grid2 size="grow" />

                <Grid2 size={6}>
                    <div style={{ width: "640px" }}>
                        <Tabs value={tabValue} onChange={handleCameraTabChange} variant="fullWidth">
                            <Tab label=<Typography>Left Camera</Typography> id="left" />
                            <Tab label=<Typography>Center Camera</Typography> id="center" />
                            <Tab label=<Typography>Right Camera</Typography> id="right" />
                        </Tabs>
                    </div>
                <CameraFeed orientation={currentCamera} />
                </Grid2>

                <Grid2 size={.6} />

                <Grid2 size={5.4}>
                        <Container style={{display:"flex", justifyContent:"space-between", padding:"0px"}}>
                            <Button variant="contained" style={buttonStyle} onClick={() => changeSelectedButton("add")} color={selectedButton==="add" ? "secondary" : "primary"}>
                                <Typography variant="h5">Add New Track</Typography>
                            </Button>
                            <Button variant="contained" style={buttonStyle} onClick={() => changeSelectedButton("select")} color={selectedButton==="select" ? "secondary" : "primary"}>
                                <Typography variant="h5" >Select Track</Typography>
                            </Button>
                            <Button variant="contained" style={buttonStyle} onClick={() => changeSelectedButton("run")} color={selectedButton==="run" ? "secondary" : "primary"}>
                                <Typography variant="h5">Run Track</Typography>
                            </Button>

                        </Container>

                        {getMenuComponent()}
                        
                </Grid2>

                <Grid2 size="grow" />
                <Grid2 size={0} />

                <Grid2 size={4}/>
                <Grid2 size={12}>
                    <Typography variant="h5">
                        Current Track: {
                            trackName === "" ? "None" : trackName
                        }
                    </Typography>
                </Grid2>

            </Grid2>
        </>
    );
}

