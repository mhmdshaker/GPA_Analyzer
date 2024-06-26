import React from 'react';
import Dialog from '@material-ui/core/Dialog';
import Button from '@material-ui/core/Button';
import Autocomplete from '@material-ui/lab/Autocomplete';
import TextField from '@material-ui/core/TextField';
import Box from '@material-ui/core/Box';
import Typography from '@material-ui/core/Typography';
import { useState, useEffect } from 'react';
//for the token:
import { getUserToken, saveUserToken, clearUserToken } from '../localStorage';

function Home() {
  const [userToken, setUserToken] = useState(getUserToken());
  const [signIn, setSignIn] = useState(false);
  const [signUp, setSignUp] = useState(false);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [courseName, setCourseName] = useState('');
  const [courseSearchResults, setCourseSearchResults] = useState([]);
  const [semester, setSemester] = useState('');
  const [semesterSearchResults, setSemesterSearchResults] = useState([]);
  const [grade, setGrade] = useState(''); //grade to be added
  const [gpa, setGpa] = useState(0);
  const [gradeChanged, setGradeChanged] = useState(false);
  const [grades, setGrades] = useState([]); //grades to be displayed
  const Server = 'http://localhost:5000';

  //Effects:
  useEffect(() => {
    console.log('here');
    setGrades([]);
    console.log(grades);
  }, [userToken]);

  useEffect(() => {
    const fetchInitialSemesterOptions = async () => {
      const response = await fetch(`${Server}/semesters_search?name=`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });
      const data = await response.json();
      setSemesterSearchResults(data);
    };

    fetchInitialSemesterOptions();
  }, []);

  useEffect(() => {
    const fetchInitialCourseOptions = async () => {
      if (semester) {
        const response = await fetch(
          `${Server}/courses_search?name=&semester=${semester}`,
          {
            method: 'GET',
            headers: {
              'Content-Type': 'application/json',
            },
          }
        );
        const data = await response.json();
        setCourseSearchResults(data);
      }
    };
    fetchInitialCourseOptions();
  }, [semester]);

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
    if (userToken) {
      fetchGpa();
    }
  }, [userToken, gradeChanged]);

  useEffect(() => {
    const fetchGrades = async () => {
      try {
        const response = await fetch(`${Server}/grades`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${userToken}`,
          },
        });
        const data = await response.json();
        console.log(data);
        setGrades(data);
      } catch (error) {
        console.error('Error fetching grades:', error);
      }
    };
    if (userToken) {
      fetchGrades();
    }
  }, [gpa]);

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
          Authorization: `Bearer ${userToken}`,
        },
      }
    );
    const data = await response.json();
    setCourseSearchResults(data);
  };

  const handleAddGrade = () => {
    if (semester === '') {
      alert('Please select a semester');
      return;
    } else if (courseName === '') {
      alert('Please select a course');
      return;
    } else if (grade === '') {
      alert('Please enter a grade');
      return;
    }
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
    }).then(response => {
      if (!response.ok) {
        alert('You already took the course');
        return;
      }
      response.json().then(body => {
        setGradeChanged(!gradeChanged);
      });
    });
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

  const handleSignInCloseEmpty = () => {
    setSignIn(false);
    setUsername('');
    setPassword('');
  };

  const handleSignInClose = () => {
    if (!username) {
      alert('Please enter an email');
    } else if (!password) {
      alert('Please enter a password');
    } else {
      setSignIn(false);
      signInFunction();
      setUsername('');
      setPassword('');
    }
  };

  const handleSignOut = () => {
    setUserToken(null);
    clearUserToken();
    setGpa(0);
  };

  const handleSignUpOpen = () => {
    setSignUp(true);
  };

  const handleSignUpClose = () => {
    if (!username) {
      alert('Please enter an email');
    } else if (!password) {
      alert('Please enter a password');
    } else {
      setSignUp(false);
      signUpFunction();
      setUsername('');
      setPassword('');
    }
  };

  const handleSignUpCloseEmpty = () => {
    setSignUp(false);
    setUsername('');
    setPassword('');
  };

  const handleSemesterChange = (event, value) => {
    setSemester(value);
    setCourseName('');
    searchSemesters(value);
  };

  //functions:
  const handleReplaceGrade = (semester, course, newGrade) => {
    fetch(`${Server}/replace_grade`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${userToken}`,
      },
      body: JSON.stringify({
        course: course,
        semester: semester,
        grade: newGrade,
      }),
    }).then(response =>
      response.json().then(body => {
        setGradeChanged(!gradeChanged);
      })
    );
  };

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
      .then(response => {
        if (!response.ok) {
          if (response.status === 401) {
            alert('Unauthorized: Invalid username or password');
            return;
          } else {
            alert(`Error ${response.status}: ${response.statusText}`);
            return;
          }
        }
        return response.json();
      })
      .then(body => {
        setUserToken(body.token);
        saveUserToken(body.token);
      });
  };

  const signUpFunction = () => {
    fetch(`${Server}/users`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        email: username,
        password: password,
      }),
    }).then(response => {
      if (!response.ok) {
        if (response.status === 400) {
          alert('Conflict: email already used');
          return;
        } else {
          alert(`Error ${response.status}: ${response.statusText}`);
          return;
        }
      }
      response.json();
    });
  };

  const handleDeleteCourse = (name, semester) => {
    fetch(`${Server}/delete_grade`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${userToken}`,
      },
      body: JSON.stringify({
        course: name,
        semester: semester,
      }),
    }).then(response =>
      response.json().then(body => {
        setGradeChanged(!gradeChanged);
      })
    );
  };

  return (
    <div>
      {/* Sign in button */}
      {!userToken && <Button onClick={handleSignInOpen}>Sign in</Button>}
      <Dialog open={signIn} onClose={handleSignInCloseEmpty}>
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
          }}
        >
          Sign in
        </Button>
      </Dialog>
      {/* Sign up button */}
      {!userToken && <Button onClick={handleSignUpOpen}>Sign up</Button>}
      <Dialog open={signUp} onClose={handleSignUpCloseEmpty}>
        Email:
        <input type="text" value={username} onChange={handleUsernameChange} />
        Password:
        <input
          type="password"
          value={password}
          onChange={handlePasswordChange}
        />
        <Button onClick={handleSignUpClose}>Sign up</Button>
      </Dialog>
      {userToken && <Button onClick={handleSignOut}>Sign out</Button>}
      {/* Semester */}
      <Autocomplete
        openOnFocus
        options={semesterSearchResults}
        getOptionLabel={option => option.semester}
        onInputChange={handleSemesterChange}
        renderInput={params => <TextField {...params} label="Semester" />}
      />
      {/* Course Name */}
      <Autocomplete
        openOnFocus
        options={courseSearchResults}
        getOptionLabel={option => option.name}
        onInputChange={handleCourseNameChange}
        renderInput={params => <TextField {...params} label="Course Name" />}
      />
      {userToken && (
        <input type="text" value={grade} onChange={handleGradeChange} />
      )}
      {userToken && <Button onClick={handleAddGrade}>Add Grade</Button>}
      {userToken && (
        <TextField label="GPA" value={gpa} InputProps={{ readOnly: true }} />
      )}{' '}
      {/* display grades: */}
      {userToken &&
        grades.map(semester => (
          <Box border={1} margin={1} padding={1} key={semester.semester}>
            <Typography variant="h6">{semester.semester}</Typography>
            {semester.courses.map(course => (
              <Box border={1} margin={1} padding={1} key={course.course}>
                <Typography variant="body1">
                  {course.course}: {course.grade}
                </Typography>
                <button
                  onClick={() =>
                    handleDeleteCourse(course.course, semester.semester)
                  }
                >
                  X
                </button>
                {/* replace grade: */}
                <button
                  onClick={() => {
                    // pop up button to enter new grade
                    const newGrade = prompt('Enter new grade');
                    handleReplaceGrade(
                      semester.semester,
                      course.course,
                      newGrade
                    );
                  }}
                >
                  Replace Grade
                </button>
              </Box>
            ))}
          </Box>
        ))}
    </div>
  );
}

export default Home;
