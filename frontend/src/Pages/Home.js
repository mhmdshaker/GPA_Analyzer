import React from 'react';
import Dialog from '@material-ui/core/Dialog';
import Button from '@material-ui/core/Button';
import { useState } from 'react';

function Home() {
  const [signIn, setSignIn] = useState(false);
  const [signUp, setSignUp] = useState(false);
  const handleSignInOpen = () => {
    setSignIn(true);
  };
  const handleSignInClose = () => {
    setSignIn(false);
  };
  const handleSignUpOpen = () => {
    setSignUp(true);
  };
  const handleSignUpClose = () => {
    setSignUp(false);
  };
  return (
    <div>
      <h1>Home</h1>

      {/* Sign in button */}
      <Button onClick={handleSignInOpen}>Sign in</Button>
      <Dialog open={signIn} onClose={handleSignInClose}>
        Username:
        <input type="text" />
        Password:
        <input type="text" />
        <Button onClick={handleSignInClose}>Sign in</Button>
      </Dialog>

      {/* Sign up button */}
      <Button onClick={handleSignUpOpen}>Sign up</Button>
      <Dialog open={signUp} onClose={handleSignUpClose}>
        Username:
        <input type="text" />
        Email:
        <input type="text" />
        Password:
        <input type="text" />
        <Button onClick={handleSignUpClose}>Sign up</Button>
      </Dialog>

      
    </div>
  );
}

export default Home;
