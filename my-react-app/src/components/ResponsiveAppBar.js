import React, { useEffect } from 'react';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import IconButton from '@mui/material/IconButton';
import Typography from '@mui/material/Typography';
import Menu from '@mui/material/Menu';
import MenuIcon from '@mui/icons-material/Menu';
import Container from '@mui/material/Container';
import Avatar from '@mui/material/Avatar';
import Button from '@mui/material/Button';
import Tooltip from '@mui/material/Tooltip';
import MenuItem from '@mui/material/MenuItem';
import Logo from '../photos/BOTNETLOGO.jpg';
import { useAuth0 } from '@auth0/auth0-react';
import { Link } from 'react-router-dom';
import DarkModeToggle from "react-dark-mode-toggle";


const pages = ['Home', 'Tracking List'];

const ResponsiveAppBar = () => {
  const [anchorElNav, setAnchorElNav] = React.useState(null);
  const [anchorElUser, setAnchorElUser] = React.useState(null);
  //const [selectedUserMenuItem, setSelectedUserMenuItem] = React.useState(null);
  const { logout } = useAuth0();
  const [isDarkMode, setIsDarkMode] = React.useState(() => false);
  const [text1, setText1] = React.useState();
  const [text2, setText2] = React.useState();
  const [text3, setText3] = React.useState();
  const [text4, setText4] = React.useState();

  const handleOpenNavMenu = (event) => {
    setAnchorElNav(event.currentTarget);
  };
  const handleOpenUserMenu = (event) => {
    setAnchorElUser(event.currentTarget);
  };

  const handleCloseNavMenu = () => {
    setAnchorElNav(null);
  };

  const handleCloseUserMenu = () => {
    setAnchorElUser(null);
    console.log("UserMenu Closed");
  };

  const handleProfileClick = (event) => {
    setAnchorElUser(null);
    console.log("Profile clicked");
  };

  const handleLogoutClick = (event) => {
    setAnchorElUser(null);
    console.log("Logout clicked");
    logout();
  };

  const handleHomePageClick = (event) => {
    console.log("Homepage clicked");
  }

  const handleTrackingListClick = (event) => {
    console.log("Tracking List clicked");
  }

  const handleTranslate = () => {
    console.log("herereeeeeee")
    if (localStorage.getItem("lan") == null) {
      localStorage.setItem("lan","sp");
    } else if (localStorage.getItem("lan") == "en") {
      localStorage.setItem("lan","sp");
    } else if (localStorage.getItem("lan") == "sp") {
      localStorage.setItem("lan","en");
    }
    window.location.reload(false);
  }

  useEffect(() => {
    console.log(localStorage.getItem("lan"));
    if (localStorage.getItem("lan") == null) {
      setText1("Home Page")
      setText2("My Tracking List")
      setText3("Translate")
      setText4("Log Out")
    } else if (localStorage.getItem('lan') == "sp") {
      setText1("Página principal")
      setText2("Mi Lista de seguimiento")
      setText3("Traducir")
      setText4("Niciar Sesión")
    } else { 
      setText1("Home Page")
      setText2("My Tracking List")
      setText3("Translate")
      setText4("Log Out")
    }
  }, []);
  
  return (
    <AppBar position="static">
      <Container maxWidth="xl">
        <Toolbar disableGutters>
          {/* <Typography
            variant="h6"
            noWrap
            component="div"
            sx={{ mr: 2, display: { xs: 'none', md: 'flex' } }}
          >
            BOTNET
          </Typography> */}
          <img src={Logo} alt="Logo"  width="60" height="60"/>

          <Box sx={{ flexGrow: 1, display: { xs: 'flex', md: 'none' } }}>
            <IconButton
              size="large"
              aria-label="account of current user"
              aria-controls="menu-appbar"
              aria-haspopup="true"
              onClick={handleOpenNavMenu}
              color="inherit"
            >
              <MenuIcon />
            </IconButton>
            <Menu
              id="menu-appbar"
              anchorEl={anchorElNav}
              anchorOrigin={{
                vertical: 'bottom',
                horizontal: 'left',
              }}
              keepMounted
              transformOrigin={{
                vertical: 'top',
                horizontal: 'left',
              }}
              open={Boolean(anchorElNav)}
              onClose={handleCloseNavMenu}
              sx={{
                display: { xs: 'block', md: 'none' },
              }}
            >
              {pages.map((page) => (
                <MenuItem key={page} onClick={handleCloseNavMenu}>
                  <Typography textAlign="center">{page}</Typography>
                </MenuItem>
              ))}
            </Menu>
          </Box>
          {/* <Typography
            variant="h6"
            noWrap
            component="div"
            sx={{ flexGrow: 1, display: { xs: 'flex', md: 'none' } }}
          >
            LOGO
          </Typography> */}
          <Box sx={{ flexGrow: 1, display: { xs: 'none', md: 'flex' } }}>
            <Link to="/Home">
              <Button
                // component={Link} to="./HomePage"
                onClick={handleHomePageClick}
                sx={{ my: 2, color: 'white', display: 'block' }}
              >
                {text1}
              </Button>
            </Link>
            <Link to="/TrackingList">
            <Button
                onClick={handleTrackingListClick}
                sx={{ my: 2, color: 'white', display: 'block' }}
              >
                {text2}
              </Button>
            </Link>
            <Button  sx={{ my: 2, color: 'white', display: 'block' }} onClick={handleTranslate}>
              {text3}
            </Button>

          </Box>

          <Box sx={{ flexGrow: 0 }}>
            <Tooltip title="Open settings">
              <IconButton onClick={handleOpenUserMenu} sx={{ p: 0 }}>
                <Avatar alt="Remy Sharp" src="/static/images/avatar/2.jpg" />
              </IconButton>
            </Tooltip>
            <Menu
              sx={{ mt: '45px' }}
              id="menu-appbar"
              anchorEl={anchorElUser}
              anchorOrigin={{
                vertical: 'top',
                horizontal: 'right',
              }}
              keepMounted
              transformOrigin={{
                vertical: 'top',
                horizontal: 'right',
              }}
              open={Boolean(anchorElUser)}
              onClose={handleCloseUserMenu}
            >
              <MenuItem onClick={handleLogoutClick}>
                <Typography textAlign="center">{text4}</Typography>
              </MenuItem>
            </Menu>
          </Box>
        </Toolbar>
      </Container>
    </AppBar>
  );
};
export default ResponsiveAppBar;