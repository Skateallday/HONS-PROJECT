import React from 'react';
import ReactDOM from 'react-dom';
import 'bootstrap';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import $ from 'jquery';
import './App.css';
import CreatePost from './createPost';
import CreateGroup from './createGroup';



export default class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {render:''}

  }
    create(compName, e){
      console.log(compName);
      this.setState({render:compName});
    }

    _renderSubComp(){
      switch(this.state.render){
        case 'createPost': return <CreatePost />
        case 'createGroup': return <CreateGroup />
      }
    }
  

  render(){
    return (      
    <div className="actions">
      <Button onClick={this.create.bind(this, 'createGroup')}>Create Group</Button>    
      <Button onClick={this.create.bind(this, 'createPost')}>Create Post</Button>
      {this._renderSubComp()}

    </div>

    );
  }
}


ReactDOM.render(<App />, document.getElementById('App'));



