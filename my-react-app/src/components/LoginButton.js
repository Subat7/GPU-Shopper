import React from 'react';
import Button from '@mui/material/Button';
import { useAuth0 } from '@auth0/auth0-react';
import { createTheme, ThemeProvider } from '@mui/material/styles';

const LoginButton = () => {
    
    const { loginWithRedirect } = useAuth0();
    const theme = createTheme();

  return (

    <ThemeProvider theme={theme}>
      <Button onClick={() => loginWithRedirect()}
                type="submit"
                fullWidth
                variant="contained"
                sx={{ mt: 3, mb: 2 }}
              >
                Sign In with Auth0
              </Button>
      {/* <Button onClick={() => loginWithRedirect()}>
        Log in with react 
      </Button> */}

       </ThemeProvider>
    
    
  )
}

export default LoginButton