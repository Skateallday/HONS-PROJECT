import React from 'react';
import logo from './possiblelogos.svg';
import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';


function SignUp() {
  return (
    <div className="signup">
      <div className="App-background">
        
        <div className="SignUp">
          <img src={logo} alt="logo" className="App-logo"/>
          <Form>
          <Form.Group controlId="formBasicUsername">
              <Form.Label>Username</Form.Label>
              <Form.Control type="password" placeholder="Username" />
            </Form.Group>

            
            <Form.Group controlId="formBasicPassword">
              <Form.Label>Password</Form.Label>
              <Form.Control type="password" placeholder="Password" />
            </Form.Group>
            
            <Button className="button button1" type="submit">
            Login
            </Button>
            <p>Or</p>
            <Button variant="success" type="submit">
              Register Here
            </Button>
          </Form>

        </div>  
      </div>
    </div>
  );
}

export default SignUp;
