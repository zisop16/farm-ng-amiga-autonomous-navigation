import { Box } from "@mui/material";

// 0 = left camera
// 1 = center camera
// 2 = right camera

interface CameraFeedProps {
    orientation: string,
};

export default function CameraFeed(props: CameraFeedProps) {
    return (
        <Box style={{ backgroundColor: "#000", height: "480px", width: "640px", color: "white" }}>
            <center>
            {props.orientation} camera placeholder
            </center>
        </Box>

    )
}
