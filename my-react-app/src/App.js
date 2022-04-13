import React, { useState } from "react";
//import ReactDOM from "react-dom";
import LoginButton from './components/LoginButton';
import Navbar from './components/Navbar';
import LogoutButton from "./components/LogoutButton";
import ResponsiveAppBar from "./components/ResponsiveAppBar";

import "./App.css";

function App() {

  return (
    <div>
      <ResponsiveAppBar />
      <Navbar />
      <LoginButton />
      <LogoutButton />
    </div>
  );
}

export default App;