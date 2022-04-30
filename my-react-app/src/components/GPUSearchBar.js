import * as React from 'react';
import Checkbox from '@mui/material/Checkbox';
import TextField from '@mui/material/TextField';
import Autocomplete from '@mui/material/Autocomplete';
import CheckBoxOutlineBlankIcon from '@mui/icons-material/CheckBoxOutlineBlank';
import CheckBoxIcon from '@mui/icons-material/CheckBox';

const icon = <CheckBoxOutlineBlankIcon fontSize="small" />;
const checkedIcon = <CheckBoxIcon fontSize="small" />;

export default function GPUSearchBar() {

  const handleSubmit = async (event) => {
    //Prevent page reload
    event.preventDefault();

    // var { uname, pass } = document.forms[0];

    // Find user login info
    // const userData = database.find((user) => user.username === uname.value);
    const Search = "ASUS";

    const response = await fetch ('/Searching',{
      method: 'POST',
      header:{
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({Search: Search})

    }).then(function (response) {
      return response.text();
    }).then(function (text) {
      console.log(text);
    })

    //console.log(response);
  };

  const handleChange = (event) => {
    // if (event.selected == "true" ){
    //   console.log(event.key);
    // }
    //console.log(event.aria-selected);
    
  };

  return (
    <Autocomplete
      multiple
      id="checkboxes-tags-demo"
      options={GPUs}
      disableCloseOnSelect
      getOptionLabel={(option) => option.title}
      renderOption={(props, option, { selected }) => (
        <li {...props}>
          <Checkbox
            icon={icon}
            checkedIcon={checkedIcon}
            style={{ marginRight: 8 }}
            checked={selected}
            onChange={handleSubmit}
          />
          {option.title}
        </li>
      )}
      style={{ width: 500 }}
      renderInput={(params) => (
        <TextField {...params} label="Search For GPUs in the DataBase" placeholder="Favorites" />
      )}
    />
  );
}

const GPUs = [
  { title: '2080', year: 1994 },
  { title: '3060', year: 1972 },
  { title: '3070', year: 1974 },
  { title: '3090', year: 2008 },
];