import React, { useEffect } from 'react';
import Checkbox from '@mui/material/Checkbox';
import TextField from '@mui/material/TextField';
import Autocomplete from '@mui/material/Autocomplete';
import CheckBoxOutlineBlankIcon from '@mui/icons-material/CheckBoxOutlineBlank';
import CheckBoxIcon from '@mui/icons-material/CheckBox';
import SendIcon from '@mui/icons-material/Send';
import Button from '@mui/material/Button';
import Stack from '@mui/material/Stack';
import { createTheme, ThemeProvider, useTheme } from '@mui/material/styles';
import { useAuth0 } from '@auth0/auth0-react';


const icon = <CheckBoxOutlineBlankIcon fontSize="small" />;
const checkedIcon = <CheckBoxIcon fontSize="small" />;





export default function GPUSearchBar() {

  

  const [gpus, setGpus] = React.useState([]);
  const [selectedGPU, setSelectedGPU] = React.useState();
  const [enteredText, setEnteredText] = React.useState([]);
  const [text1, setText1] = React.useState();
  const [text2, setText2] = React.useState();
  const { user } = useAuth0();

  

  // if (localStorage.getItem("lan") != "en") {
  //   setText1('Add to Tracking List')
  // } else {
  //   setText1('Agregar a la lista de seguimiento')
  // }

  

  const myTheme = createTheme({
    palette: {
      mode: 'light',
    },
  });

  const handleSubmit = async (event) => {

    const response = await fetch ('/print_api_results',{
      method: 'POST',
      header:{
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
    }).then(function (response) {
      return response.json();
    }).then(function (json) {
      console.log(json)
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


    const response = await fetch ('/addUserTracking',{
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
      setText1("Add To Tracking List")
      setText2("Search for GPUs in the Database")
    } else if (localStorage.getItem('lan') == "sp") {
      setText1("Agregar a la lista de seguimiento")
      setText2(" Buscar GPU en la base de datos")
    } else { 
      setText1("Add to Tracking List")
      setText2("Search for GPUs in the Database")
    }
    handleSubmit();
  }, []);

  const handleClick = () => {
    console.log(gpus[0]['stock']);
    handleForward();
    // window.location.reload(false);
  }

  return (
    <ThemeProvider theme={myTheme}>
      <div style={{
      position: 'absolute', left: '50%', top: '50%',
      transform: 'translate(-50%, -50%)',
      width: '80%',
  }}>
      <Stack direction="row" spacing={2} fullWidth={true}>
      <Autocomplete
            clearOnEscape={true}
            noOptionsText="Loading"
            disablePortal
            id="combo-box-demo"
            options={gpus}
            renderOption={(props, option) => {
              const {label, stock} = option;
              let color;
              if (stock == '0') {
                console.log("here")
                color = "pink"
              } else {
                color = '#C7FFC7'
              }
              return (
                <span {...props} style={{ backgroundColor: color }}>
                  {label}
                </span>
              );
            }}
            fullWidth={true}
            onChange={(event, value) => setSelectedGPU(value)} // prints the selected value
            renderInput={(params) => <TextField sx={{color: 'green'}} {...params} label={text2} />}
          />
      <Button variant="contained" endIcon={<SendIcon sx="auto"/>}
         onClick={handleClick}>
           {text1}
      </Button>
    </Stack>
    </div>
    </ThemeProvider>
    
    
    
  );
}
