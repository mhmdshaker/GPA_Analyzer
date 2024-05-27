import React from 'react';
import Dialog from '@material-ui/core/Dialog';
import Button from '@material-ui/core/Button';
import Autocomplete from '@material-ui/lab/Autocomplete';
import TextField from '@material-ui/core/TextField';
import { useState } from 'react';

function Home() {
  const [signIn, setSignIn] = useState(false);
  const [signUp, setSignUp] = useState(false);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [courseName, setCourseName] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  const [grade, setGrade] = useState('');
  const Server = 'http://localhost:5000';

  const searchCourses = async query => {
    const response = await fetch(`${Server}/courses_search?name=${query}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });
    const data = await response.json();
    setSearchResults(data);
  };

  const handleAddGrade = () => {};

  const handleCourseNameChange = (event, value) => {
    setCourseName(value);
    searchCourses(value);
  };

  const handleGradeChange = event => {
    setGrade(event.target.value);
  };

  const handleUsernameChange = event => {
    setUsername(event.target.value);
  };

  const handlePasswordChange = event => {
    setPassword(event.target.value);
  };

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
      {/* Sign in button */}
      <Button onClick={handleSignInOpen}>Sign in</Button>
      <Dialog open={signIn} onClose={handleSignInClose}>
        Username:
        <input type="text" value={username} onChange={handleUsernameChange} />
        Password:
        <input
          type="password"
          value={password}
          onChange={handlePasswordChange}
        />
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

      <Autocomplete
        options={searchResults}
        getOptionLabel={option => option.name}
        onInputChange={handleCourseNameChange}
        renderInput={params => <TextField {...params} label="Course Name" />}
      />

      <input type="text" value={grade} onChange={handleGradeChange} />
      <Button onClick={handleAddGrade}>Add Grade</Button>
    </div>
  );
}

export default Home;
