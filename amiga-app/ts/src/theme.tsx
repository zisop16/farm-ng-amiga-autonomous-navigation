import { createTheme } from '@mui/material/styles';
import { } from '@mui/material/colors';

const theme = createTheme({
    palette: {
        mode: 'dark',
        primary: {
            main: "#6feafc",
            contrastText: "#000"
        },
        secondary: {
            main: "#0000FF",
            contrastText: "#FFF"
        },
        background: {
            default: "#363636"
        }
    },
});

export default theme;
