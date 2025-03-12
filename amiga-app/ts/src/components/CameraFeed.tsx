import { Box } from "@mui/material";

// 0 = left camera
// 1 = center camera
// 2 = right camera

export default function CameraFeed(props: any) {
    return (
        <Box style={{ backgroundColor: "#000", height: "480px", width: "640px", color: "white" }}>
            <center>
            {props.orientation} camera placeholder
            </center>
        </Box>

    )
}
