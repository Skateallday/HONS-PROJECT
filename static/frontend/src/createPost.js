import React from 'react';
import 'bootstrap';
import './App.css';
import Button from 'react-bootstrap/Button';

var $ = require('jquery');

export default class CreatePost extends React.Component {    
    constructor(props) {
        super(props);
        this.state = {title: '', posted:'Title of the post', Desciption: '', posted:'Description of the post', finishedPost: ' '};        
        this.handleTitle = this.handleTitle.bind(this);
        this.handleDesp = this.handleDesp.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
      }   

      handleTitle(event) {
        this.setState({title: event.target.value});
        this.setState({posted: event.target.value});
        $.get(window.location.href + '/Post', (value) => {
            console.log('Title: ' +this.state.title);
          });
        
      }   
      
      handleDesp(event) {
        this.setState({Desciption: event.target.value});
        this.setState({posted: event.target.value});
        $.get(window.location.href + '/Post', (value) => {
            console.log('Description: ' + this.state.Desciption);
          });
        
      }  
      handleSubmit(event) {
        event.preventDefault();
        console.log(event);
        this.setState({finishedPost: (this.state.title + '\n' + this.state.Desciption)});
      }   
    
 
      render(){
        return(
            <div>
            <form className="form" >
              <fieldset>
                <legend>New Post</legend>    
                <input ref="postTitle" type="text" value={this.state.title} placeholder="Post Title" onChange={this.handleTitle} />    
                <input ref="postDesp" type="text" value={this.state.Desciption} placeholder="Post Desciption" onChange={this.handleDesp} />    

                <Button onClick={this.handleSubmit} className="button button1">Post!</Button>
                </fieldset>
            </form>
        <p>{this.state.finishedPost}</p>
        </div> );};
      }
  


