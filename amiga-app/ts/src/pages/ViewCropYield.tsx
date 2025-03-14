import { Container, Grid2, Typography } from "@mui/material";
import BackButton from "../components/BackButton";

export default function ViewCropYield() {
    return (
        <>
            <Grid2 container spacing={0} rowSpacing={20} style={{ margin: "30px 0 0 30px" }}>
                <Grid2 size={1} display="flex" justifyContent="center" alignItems="center">
                    <BackButton />
                </Grid2>
                <Grid2 size={10} display="flex" justifyContent="center" alignItems="center">
                    <Typography variant="h2">View Crop Yield</Typography>
                </Grid2>
                <Container>
                    <Typography>Placeholder</Typography>
                </Container>

            </Grid2>
        </>

    )
}
