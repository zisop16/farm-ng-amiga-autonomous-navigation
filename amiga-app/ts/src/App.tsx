import { BrowserRouter, Route, Routes } from "react-router";
import './App.css'
import Home from './pages/Home'
import TrackSelect from './pages/TrackSelect'
import ViewCropYield from "./pages/ViewCropYield";
<<<<<<< HEAD
import TrackCreate from "./pages/TrackCreate";
=======
>>>>>>> 2ffd193a1d4f6da38c883c3d7711c1e2ad66af85
import { useEffect } from "react";

function App() {

    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<Home />}/>
                <Route path="/TrackSelect" element={<TrackSelect />}/>
                <Route path="/ViewCropYield" element={<ViewCropYield />}/>
            </Routes>
        </BrowserRouter>
    )
}

export default App
