import { Box } from "@mui/material";

// 0 = left camera
// 1 = center camera
// 2 = right camera

interface CameraFeedProps {
    orientation: string,
};

function orientationToIp(orientation: string) {
    let baseIp = "http://10.95.76"
    switch (orientation) {
        case "left":
            baseIp += ".11"
            break
         case "center":
            baseIp += ".12"
            break
        case "right":
            baseIp += ".13"
            break
        default:
            baseIp += ".12"
    }
    baseIp += ":5000/rgb"
    return baseIp
}

export default function CameraFeed(props: CameraFeedProps) {
    return (
        <Box style={{ backgroundColor: "#000", height: "400px", width: "640px", color: "white" }}>
            <img src={orientationToIp(props.orientation)}/>
        </Box>

    )
}
