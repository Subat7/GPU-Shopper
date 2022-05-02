import React, { useEffect } from 'react';
import Checkbox from '@mui/material/Checkbox';
import TextField from '@mui/material/TextField';
import Autocomplete from '@mui/material/Autocomplete';
import CheckBoxOutlineBlankIcon from '@mui/icons-material/CheckBoxOutlineBlank';
import CheckBoxIcon from '@mui/icons-material/CheckBox';
import SendIcon from '@mui/icons-material/Send';
import Button from '@mui/material/Button';
import { styled } from '@mui/material/styles';
import Box from '@mui/material/Box';
import Paper from '@mui/material/Paper';
import Grid from '@mui/material/Grid';
import Stack from '@mui/material/Stack';
import CircularProgress from '@mui/material/CircularProgress';

const icon = <CheckBoxOutlineBlankIcon fontSize="small" />;
const checkedIcon = <CheckBoxIcon fontSize="small" />;



export default function GPUSearchBar() {

  const [gpus, setGpus] = React.useState([]);
  const [selectedGPU, setSelectedGPU] = React.useState();
  const [enteredText, setEnteredText] = React.useState([]);

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
      setGpus(json);
    })
  };

  const handleForward = async (event) => {

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
    handleSubmit();
  }, []);

  const handleClick = () => {
    handleForward();
    // window.location.reload(false);
  }

  return (
    <div style={{
      position: 'absolute', left: '50%', top: '50%',
      transform: 'translate(-50%, -50%)'
  }}>
      <Stack direction="row" spacing={2}>
      <Autocomplete
            disablePortal
            id="combo-box-demo"
            options={gpus}
            sx={{ width: 1000 }}
            onChange={(event, value) => setSelectedGPU(value)} // prints the selected value
            renderInput={(params) => <TextField {...params} label="Search for GPUs in the Database" />}
          />
      <Button variant="contained" endIcon={<SendIcon sx="auto"/>}
         onClick={handleClick}>
          Add to Tracking List
      </Button>
    </Stack>
    </div>
    
    
  );
}
