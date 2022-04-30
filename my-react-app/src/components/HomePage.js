import React, { useEffect } from 'react';
import ResponsiveAppBar from './ResponsiveAppBar';
import GPUSearchBar from './GPUSearchBar';
import { useAuth0 } from '@auth0/auth0-react';


const HomePage = () => {
  const { user } = useAuth0();

  const handleSubmit = async (event) => {
    //Prevent page reload


    // var { uname, pass } = document.forms[0];

    // Find user login info
    // const userData = database.find((user) => user.username === uname.value);
    const user_email = user.email;

    const response = await fetch ('/update_users',{
      method: 'POST',
      header:{
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({UserEmail: user_email})
    });

    console.log("sending user email forward");
  };

  useEffect(() => {
    handleSubmit();
  }, []);

  return (
    <div>
      <ResponsiveAppBar />
      <div
        style={{
          position: 'absolute', left: '50%', top: '50%',
          transform: 'translate(-50%, -50%)'
      }}
      >
        <GPUSearchBar />
      </div>

    </div>
  )
}

export default HomePage