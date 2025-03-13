import { Button, Grid2, Stack, Tab, Tabs, Typography } from "@mui/material";
import BackButton from "../components/BackButton";
import CameraFeed from "../components/CameraFeed";
import React from "react";

export default function TrackSelect() {
    const [tabValue, setTabValue] = React.useState(1);
    const [currentCamera, setCurrentCamera] = React.useState("center");

    const handleChange = (event: React.SyntheticEvent, newValue: number) => {
        setTabValue(newValue);
        setCurrentCamera(event.currentTarget.id)
    };

    return (
        <>
            <Grid2 container spacing={0} style={{ margin: "30px 0 0 30px" }} >
                <Grid2 size={1} display="flex" justifyContent="center" alignItems="center">
                    <BackButton />
                </Grid2>
                <Grid2 size={10} display="flex" justifyContent="center" alignItems="center">
                    <Typography variant="h2">Track Select</Typography>
                </Grid2>

                <Grid2 size={12} height="30px" />

                <Grid2 size={12}>
                    <div style={{ width: "640px" }}>
                        <Tabs value={tabValue} onChange={handleChange} variant="fullWidth">
                            <Tab label=<Typography>Left Camera</Typography> id="left" />
                            <Tab label=<Typography>Center Camera</Typography> id="center" />
                            <Tab label=<Typography>Right Camera</Typography> id="right" />
                        </Tabs>
                    </div>
                </Grid2>

                <CameraFeed orientation={currentCamera} />

                <Grid2 size={.1} />

                <Grid2 size="auto">
                    <Stack rowGap={1} spacing="auto" sx={{ flexGrow: 1, justifyContent: 'space-between', height: '100%' }}>
                        <Button variant="contained" style={{ width: "120px", height: "120px", borderRadius: "4px" }}>
                            <Typography>Add New Track</Typography>

                        </Button>
                        <Button variant="contained" style={{ width: "120px", height: "120px", borderRadius: "4px" }}>
                            <Typography>Run Track</Typography>
                        </Button>
                        <Button variant="contained" style={{ width: "120px", height: "120px", borderRadius: "4px" }}>
                            <Typography>View Track</Typography>
                        </Button>
                    </Stack>
                </Grid2>

                <Grid2 size={3} />

                <Grid2>
                    <Typography variant="h5">Current Track: None</Typography>
                </Grid2>

            </Grid2>
        </>
    )
}
