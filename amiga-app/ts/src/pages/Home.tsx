import { Button, Container, Grid2, Typography } from "@mui/material";
import '../App.css'
import ExitButton from '../components/ExitButton'
import { useNavigate } from "react-router";

export default function Home() {
    let navigate = useNavigate()
    let handleClick = () => {
        navigate("/TrackSelect")
    }

    return (
        <>
            <Grid2 container spacing={0} rowSpacing={20} style={{ margin: "30px 0 0 30px" }}>
                <Grid2 size={1} display="flex" justifyContent="center" alignItems="center">
                    <ExitButton />
                </Grid2>
                <Grid2 size={10} display="flex" justifyContent="center" alignItems="center">
                    <Typography variant="h2">NavLogger</Typography>
                </Grid2>
                <Container>
                    <center>
                        <div style={{ display: "flex", justifyContent: "center", marginTop: "0%" }}>
                            <div>
                                <Button variant="contained" id="navButton" onClick={handleClick} >
                                    <Typography variant="h5">Track Select</Typography>

                                </Button>
                                <Button variant="contained" id="navButton">
                                    <Typography variant="h5">View Crop Yield</Typography>
                                </Button>
                            </div>
                        </div>
                    </center>
                </Container>

            </Grid2>
        </>

    )
}
