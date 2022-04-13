import React from "react";
import SignInSide from './components/LoginPage';
import CircularProgress from '@mui/material/CircularProgress';
import Box from '@mui/material/Box';
import { useAuth0 } from '@auth0/auth0-react';
import HomePage from './components/HomePage';

import "./App.css";

function App() {

  const { isAuthenticated, isLoading } = useAuth0();

  if (isLoading) {
    return (
    <Box sx={{ top: 0,
      left: 0,
      bottom: 0,
      right: 0,
      position: 'absolute',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center', }}>
      <CircularProgress />
    </Box>)
  }

  if (isAuthenticated) {
    return <HomePage />
  }
  return <SignInSide /> ;
  
}

export default App;