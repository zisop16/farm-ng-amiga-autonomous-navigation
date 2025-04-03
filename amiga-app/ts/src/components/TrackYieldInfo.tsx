// src/components/TrackYieldInfo.tsx
import { Box, Typography } from "@mui/material";

interface TrackYieldInfoProps {
    date: string;
    totalYield: number;
    pathLength: number;
}

export default function TrackYieldInfo({ date, totalYield, pathLength }: TrackYieldInfoProps) {
    return (
        <Box
            sx={{
                border: "2px solid black",
                borderRadius: 4,
                padding: 4,
                width: "100%",
                maxWidth: 400,
                marginTop: 2,
            }}
        >
            <Typography>Date collected: {date}</Typography>
            <Typography>Total Yield: {totalYield} grams</Typography>
            <Typography>Path Length: {pathLength} m</Typography>
        </Box>
    );
}

