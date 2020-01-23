import React from 'react';
import 'bootstrap';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link
} from "react-router-dom";
import $ from 'jquery';

import logo from './login2.jpg'
import './App.css';


export default class App extends React.Component {
  constructor(props) {
    super(props);
    
  // This binding is necessary to make `this` work in the callback
  this.getPythonSignUp = this.getPythonSignUp.bind(this);
  }
  getPythonSignUp() {
    $.get(window.location.href + 'register', (data) => {
      console.log('working');
  });
        
    };
    

render(){
  return (
    
      <div className="App">
        <div className="LoginBackground">  
    <Router>       
            {/* A <Switch> looks through its children <Route>s and
                renders the first one that matches the current URL. */}
           
          
 <Switch>
              <Route path="/LogIn">
                <LogIn />
              </Route>
              <Route path="/SignUp">
                <SignUp />
              </Route>
              
            </Switch>
        </Router>
        </div>
        </div>
  );}
}

function getPythonSignUp(){
  $.get(window.location.href + 'register', (data) => {
    console.log('working');
});
      
}

function LogIn() {
  return (
        
        <div className="SignUpContainer">
          <img src={logo} alt="logo" className="App-logo"/>
          <Form className="form">
          <Form.Group controlId="formBasicUsername">
          <Form.Text className="text-muted">
                Welcome Back!
              </Form.Text>
              </Form.Group>
              <Form.Group>
              <Form.Label>Username / Email</Form.Label>
              <Form.Control type="password" placeholder="Username" />
              </Form.Group>
              <Form.Group>
              <Form.Text className="text-muted">
                We'll never share your email with anyone else.
              </Form.Text>
            </Form.Group>

            
            <Form.Group controlId="formBasicPassword">
              <Form.Label>Password</Form.Label>
              <Form.Control type="password" placeholder="Password" />
            </Form.Group>
            
            <Button  className="button button1" type="submit" onClick={getPythonSignUp}>
            Login
            </Button>
            
            <p>Or</p>
            <Button className="button button1" type="submit">
            <Link to="/SignUp">Sign Up</Link>
            </Button>
          </Form>

        </div> 
  );
}


function SignUp() {
  return(
        
        <div className="SignUpContainer">
          <img src={logo} alt="logo" className="App-logo"/>
          <Form>
          <Form.Group controlId="formBasicUsername"> 
          
              <Form.Label>Username</Form.Label>
              <Form.Control type="password" placeholder="Username" />
            </Form.Group>

            <Form.Group controlId="formBasicEmail">
              <Form.Label>Email address</Form.Label>
              <Form.Control type="email" placeholder="Enter email" />
              </Form.Group>
              <Form.Group>
              <Form.Text className="text-muted">
                We'll never share your email with anyone else.
              </Form.Text>
            </Form.Group>

            <Form.Group controlId="formBasicPassword">
              <Form.Label>Password</Form.Label>
              <Form.Control type="password" placeholder="Password" />
            </Form.Group>
            
            <Button  className="button button1" type="submit" onClick={getPythonSignUp}>
            Sign Up Now!
            </Button>
            <p>Or</p>
            <Button className="button button1" title="Go to Details">
            <Link to="/LogIn">LogIn</Link>
            </Button>
          </Form>

        </div> 
  );
  };

