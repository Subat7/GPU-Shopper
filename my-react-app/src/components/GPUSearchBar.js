import React, { useEffect } from 'react';
import Checkbox from '@mui/material/Checkbox';
import TextField from '@mui/material/TextField';
import Autocomplete from '@mui/material/Autocomplete';
import CheckBoxOutlineBlankIcon from '@mui/icons-material/CheckBoxOutlineBlank';
import CheckBoxIcon from '@mui/icons-material/CheckBox';

const icon = <CheckBoxOutlineBlankIcon fontSize="small" />;
const checkedIcon = <CheckBoxIcon fontSize="small" />;



export default function GPUSearchBar() {

  const [gpus, setGpus] = React.useState([]);

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

  useEffect(() => {
    handleSubmit();
  }, []);


  return (
    <Autocomplete
      disablePortal
      id="combo-box-demo"
      options={gpus}
      sx={{ width: 1000 }}
      renderInput={(params) => <TextField {...params} label="Search for GPUs in the Database" />}
    />
  );
}
