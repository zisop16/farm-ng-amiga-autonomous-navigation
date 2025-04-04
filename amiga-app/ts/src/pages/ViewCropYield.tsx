import { Container, Grid, Typography } from "@mui/material";
import BackButton from "../components/BackButton";
import TrackYieldSelect from "../components/TrackYieldSelect";
import TrackYieldInfo from "../components/TrackYieldInfo";
import { useState } from "react";

interface TrackRun {
    date: string,
    totalYield: number,
    pathLength: number
};

const dummyRuns = ["Path Run Name 1", "Path Run Name 2", "Path Run Name 3"];
const dummyInfo: {[id: string]: TrackRun}  = {
    "Path Run Name 1": { date: "04/01/25", totalYield: 200, pathLength: 15 },
    "Path Run Name 2": { date: "04/02/25", totalYield: 180, pathLength: 12 },
    "Path Run Name 3": { date: "04/03/25", totalYield: 210, pathLength: 17 }
};

export default function ViewCropYield() {
    const [selectedRun, setSelectedRun] = useState<string>("");

    const selectedInfo: TrackRun = dummyInfo[selectedRun];

    return (
        <Container sx={{ mt: 4 }}>
            <Grid container spacing={4}>
                <Grid item xs={12} display="flex" alignItems="center">
                    <BackButton />
                    <Typography variant="h4" sx={{ ml: 2 }}>
                        View Crop Yield
                    </Typography>
                </Grid>

                <Grid item xs={12} md={4}>
                    <TrackYieldSelect
                        runs={dummyRuns}
                        selectedRun={selectedRun}
                        onSelectRun={setSelectedRun}
                    />
                </Grid>

                <Grid item xs={12} md={8}>
                    {selectedRun ? (
                        <TrackYieldInfo
                            date={selectedInfo.date}
                            totalYield={selectedInfo.totalYield}
                            pathLength={selectedInfo.pathLength}
                        />
                    ) : (
                        <Typography variant="body1" mt={2}>
                            Select a path run to view its yield info.
                        </Typography>
                    )}
                </Grid>
            </Grid>
        </Container>
    );
}
