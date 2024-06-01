import React from 'react';
import Dialog from '@material-ui/core/Dialog';
import Button from '@material-ui/core/Button';
import Autocomplete from '@material-ui/lab/Autocomplete';
import TextField from '@material-ui/core/TextField';
import { useState, useEffect } from 'react';

function Home() {
  const [userToken, setUserToken] = useState();
  const [signIn, setSignIn] = useState(false);
  const [signUp, setSignUp] = useState(false);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [courseName, setCourseName] = useState('');
  const [courseSearchResults, setCourseSearchResults] = useState([]);
  const [semester, setSemester] = useState('');
  const [semesterSearchResults, setSemesterSearchResults] = useState([]);
  const [grade, setGrade] = useState('');
  const [gpa, setGpa] = useState(0);
  const [gradeChanged, setGradeChanged] = useState(false);
  const Server = 'http://localhost:5000';

  //Effects:
  useEffect(() => {
    const fetchGpa = async () => {
      const response = await fetch(`${Server}/gpa`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${userToken}`,
        },
      });
      const data = await response.json();
      setGpa(data.gpa);
    };

    fetchGpa();
  }, [userToken, gradeChanged]);

  const searchSemesters = async query => {
    const response = await fetch(`${Server}/semesters_search?name=${query}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });
    const data = await response.json();
    setSemesterSearchResults(data);
  };

  const searchCourses = async (query1, query2) => {
    const response = await fetch(
      `${Server}/courses_search?name=${query1}&semester=${query2}`,
      {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      }
    );
    const data = await response.json();
    setCourseSearchResults(data);
  };
  const handleAddGrade = () => {
    console.log(userToken);
    fetch(`${Server}/add_grade`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${userToken}`,
      },
      body: JSON.stringify({
        course: courseName,
        grade: grade,
        semester: semester,
      }),
    }).then(response =>
      response.json().then(body => {
        setGradeChanged(!gradeChanged);
      })
    );
  };

  const handleCourseNameChange = (event, value) => {
    if (semester === '') {
      console.log('Semester not selected');
      return;
    }
    setCourseName(value);
    searchCourses(value, semester);
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

  const handleSemesterChange = (event, value) => {
    setSemester(value);
    searchSemesters(value);
  };

  //functions:
  const signInFunction = () => {
    fetch(`${Server}/sign_in`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        email: username,
        password: password,
      }),
    })
      .then(response => response.json())
      .then(body => {
        setUserToken(body.token);
      });
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
        <Button
          onClick={() => {
            handleSignInClose();
            signInFunction();
          }}
        >
          Sign in
        </Button>
      </Dialog>
      {/* Sign up button */}
      <Button onClick={handleSignUpOpen}>Sign up</Button>
      <Dialog open={signUp} onClose={handleSignUpClose}>
        Email:
        <input type="text" />
        Password:
        <input type="text" />
        <Button onClick={handleSignUpClose}>Sign up</Button>
      </Dialog>
      {/* Semester */}
      <Autocomplete
        options={semesterSearchResults}
        getOptionLabel={option => option.semester}
        onInputChange={handleSemesterChange}
        renderInput={params => <TextField {...params} label="Semester" />}
      />
      {/* Course Name */}
      <Autocomplete
        options={courseSearchResults}
        getOptionLabel={option => option.name}
        onInputChange={handleCourseNameChange}
        renderInput={params => <TextField {...params} label="Course Name" />}
      />
      <input type="text" value={grade} onChange={handleGradeChange} />
      <Button onClick={handleAddGrade}>Add Grade</Button>
      <TextField label="GPA" value={gpa} InputProps={{ readOnly: true }} />{' '}
    </div>
  );
}

export default Home;
