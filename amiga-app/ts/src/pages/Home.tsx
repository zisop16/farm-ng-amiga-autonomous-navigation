import { Button, Container, Paper } from "@mui/material";
import '../App.css'
import ExitButton from '../components/ExitButton'
import { useNavigate } from "react-router";

export default function Home() {
    let navigate = useNavigate()
    let handleClick = () => {
        navigate("/PathSelect")
    }
    let paperPadding = "20px";
    return (
        <>
            <ExitButton/>
            <Container>
                <center>
                        <h1 style={{ fontSize: "60px", paddingBottom: paperPadding}}>NavLogger</h1>
                        <div style={{ display: "flex", justifyContent: "center", marginTop: "0%" }}>
                            <div>
                                <Button variant="contained" id="navButton" onClick={handleClick} >Path Select</Button>
                                <Button variant="contained" id="navButton">View Crop Yield</Button>
                            </div>
                        </div>
                </center>
            </Container>
            {/*</div>*/}
        </>

    )
}
