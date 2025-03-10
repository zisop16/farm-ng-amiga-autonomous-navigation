import { Button } from "@mui/material";
import '../App.css'
import ExitButton from '../components/ExitButton'
import { useNavigate } from "react-router";

export default function Home() {
    let navigate = useNavigate()
    let handleClick = () => {
        navigate("/PathSelect")
    }
    return (
        <>
            <div style={{ height: "100vh", width: "100vw" }}>
                <ExitButton/>
                <center style={{ transform: "translateY(65px)" }}>
                    <h1 style={{ fontSize: "60px" }}>NavLogger</h1>
                </center>
                <div style={{ display: "flex", justifyContent: "center", marginTop: "15%" }}>
                    <div>
                        <Button variant="contained" id="navButton" onClick={handleClick} >Path Select</Button>
                        <Button variant="contained" id="navButton">View Crop Yield</Button>
                    </div>
                </div>
            </div>
        </>

    )
}
