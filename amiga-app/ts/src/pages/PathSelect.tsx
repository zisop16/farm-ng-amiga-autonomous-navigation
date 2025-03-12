import { Box, Button, Container, Grid2, Stack, Tab, Tabs, Typography } from "@mui/material";
import BackButton from "../components/BackButton";
import CameraFeed from "../components/CameraFeed";
import React from "react";

export default function PathSelect() {
    const [value, setValue] = React.useState(1);

    const handleChange = (_, newValue: number) => {
        setValue(newValue);
    };

    function indexToCameraName(ind: Number) {
        switch (ind) {
            case 0: return "left";
            case 1: return "center";
            case 2: return "right";
        }
    }

    return (
        <>
            <Grid2 container spacing={0} style={{ margin: "30px 0 0 30px" }} rowSpacing={3}>
                <Grid2 size={1} display="flex" justifyContent="center" alignItems="center">
                    <BackButton />
                </Grid2>
                <Grid2 size={10} display="flex" justifyContent="center" alignItems="center">
                    <Typography variant="h2">Path Select</Typography>
                </Grid2>



                <Grid2 size="auto" minHeight={480}>
                    <Tabs value={value} onChange={handleChange} aria-label="basic tabs example">
                        <Tab label="Left Camera" />
                        <Tab label="Center Camera" />
                        <Tab label="Right Camera" />
                    </Tabs>
                    <CameraFeed orientation={indexToCameraName(value)} />
                </Grid2>

                <Grid2 size={.1} />

                <Grid2 size={1.3}>
                    <Stack rowGap={1} spacing={3} style={{marginTop:"75px"}} >
                        <Button variant="contained" style={{height: "120px", borderRadius:"4px"}}>Add New Track</Button>
                        <Button variant="contained" style={{height: "120px", borderRadius:"4px"}}>Run Track</Button>
                        <Button variant="contained" style={{height: "120px", borderRadius:"4px"}}>View Track</Button>
                    </Stack>
                </Grid2>

                <Grid2 size={3}/>

                <Grid2>
                    <Typography variant="h5" >Current Path: None</Typography>
                </Grid2>

            </Grid2>
        </>
    )
}
