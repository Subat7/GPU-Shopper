import React from 'react';
import ResponsiveAppBar from './ResponsiveAppBar';
import GPUSearchBar from './GPUSearchBar';

const HomePage = () => {
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