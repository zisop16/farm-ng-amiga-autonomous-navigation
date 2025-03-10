import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter, Route, Routes } from "react-router";
import './App.css'
import Home from './pages/Home'
import PathSelect from './pages/PathSelect'

function App() {

    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<Home />}>
                    <Route index element={<PathSelect />} />
                </Route>
            </Routes>
        </BrowserRouter>
    )
}

export default App
