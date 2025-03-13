import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter, Route, Routes } from "react-router";
import './App.css'
import Home from './pages/Home'
import TrackSelect from './pages/TrackSelect'

function App() {

    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<Home />}> 
                </Route>
                <Route path="/TrackSelect" element={<TrackSelect />}>
                </Route>
            </Routes>
        </BrowserRouter>
    )
}

export default App
