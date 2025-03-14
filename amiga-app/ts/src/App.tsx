import { BrowserRouter, Route, Routes } from "react-router";
import './App.css'
import Home from './pages/Home'
import TrackSelect from './pages/TrackSelect'
import ViewCropYield from "./pages/ViewCropYield";
import TrackCreate from "./pages/TrackCreate";

function App() {

    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<Home />}/>
                <Route path="/TrackSelect" element={<TrackSelect />}/>
                <Route path="/ViewCropYield" element={<ViewCropYield />}/>
                <Route path="/TrackCreate" element={<TrackCreate />}/>
            </Routes>
        </BrowserRouter>
    )
}

export default App
