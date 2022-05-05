import React, { useEffect } from 'react';
import Stack from '@mui/material/Stack';
import TextField from '@mui/material/TextField';
import Autocomplete from '@mui/material/Autocomplete';
import SendIcon from '@mui/icons-material/Send';
import Button from '@mui/material/Button';
import { useAuth0 } from '@auth0/auth0-react';
import Snackbar from '@mui/material/Snackbar';
import MuiAlert from '@mui/material/Alert';
import { createTheme, ThemeProvider, useTheme } from '@mui/material/styles';

const TrackingList = () => {

    const [gpus, setGpus] = React.useState([]);
    const [selectedGPU, setSelectedGPU] = React.useState();
    const [text1, setText1] = React.useState();
    const [text2, setText2] = React.useState();
    const [open, setOpen] = React.useState(false);
    const { user } = useAuth0();
    const [text3, setText3] = React.useState();
    const [text4, setText4] = React.useState();

    const myTheme = createTheme({
      palette: {
        mode: 'light',
      },
    });

    const Alert = React.forwardRef(function Alert(props, ref) {
      return <MuiAlert elevation={6} ref={ref} variant="filled" {...props} />;
    });

    const handleClose = () => {
      setOpen(false);
    }

    const handleSubmit = async (event) => {

      const user_email = user.email;
    
      const response1 = await fetch ('/update_users',{
        method: 'POST',
        header:{
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({UserEmail:user_email})
      });

        const response = await fetch ('/retrieveTrackingList',{
          method: 'POST',
          header:{
            'Accept': 'application/json',
            'Content-Type': 'application/json'
          },
        }).then(function (response) {
          return response.json();
        }).then(function (json) {
          setGpus(json);
        })
      };
    
    const handleForward = async (event) => {

      const user_email = user.email;
    
      const response1 = await fetch ('/update_users',{
        method: 'POST',
        header:{
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({UserEmail:user_email})
      });

    const response = await fetch ('/removeUserTracking',{
        method: 'POST',
        header:{
        'Accept': 'application/json',
        'Content-Type': 'application/json'
        },
        body: JSON.stringify({selectedGPU})
    });
    };

    useEffect(() => {
      console.log(localStorage.getItem("lan"));
      if (localStorage.getItem("lan") == null) {
        setText1("Search for GPUs in your Tracking List")
        setText2("Remove From Tracking List")
        setText3("Success!")
        setText4("Loading")
      } else if (localStorage.getItem('lan') == "sp") {
        setText1("Buscar gpus en la lista de seguimiento")
        setText2("Eliminar de la lista de seguimiento")
        setText3("éxito")
        setText4("cargando")
      } else { 
        setText1("Search for GPUs in your Tracking List")
        setText2("Remove From Tracking List")
        setText3("Success!")
        setText4("Loading")
      }
        handleSubmit();
    }, []);

    const handleClick = () => {
        setOpen(true);
        handleForward();
        for (let i = 0; i < gpus.length; i++) {
            if(gpus[i] == selectedGPU) {
                delete gpus[i];
                console.log(selectedGPU);
            }
        }
        setSelectedGPU();
        console.log(gpus);
        // window.location.reload(false);

      }

  return (
    <ThemeProvider theme={myTheme}>
      <div>
      <Snackbar anchorOrigin={ {vertical: 'top', horizontal: 'center'}} open={open} autoHideDuration={3000} onClose={handleClose}>
        <Alert onClose={handleClose} severity="success" sx={{ width: '100%' }}>
          {text3}
        </Alert>
      </Snackbar>
      </div>
      <div style={{
        position: 'absolute', left: '50%', top: '50%',
        transform: 'translate(-50%, -50%)',
        width: '80%'
    }}>
        <Stack direction="row" spacing={2}>
        <Autocomplete
              clearOnEscape={true}
              noOptionsText="Loading"
              disablePortal
              id="combo-box-demo"
              options={gpus}
              fullWidth={true}
              onChange={(event, value) => setSelectedGPU(value)} // prints the selected value
              renderInput={(params) => <TextField {...params} label={text1} />}
            />
        <Button variant="contained" endIcon={<SendIcon sx="auto"/>}
           onClick={handleClick}>
             {text2}
            
        </Button>
      </Stack>
      </div>
    </ThemeProvider>
    
    
  )
}

export default TrackingList