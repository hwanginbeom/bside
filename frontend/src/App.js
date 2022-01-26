//frontend/src/app.js
import React, { Component } from 'react';
import GoogleLogin from 'react-google-login';
import axios from 'axios'

const clientId = "774738321836-vl1oi9dvoefg5mpjhijoaic2ond37l2a.apps.googleusercontent.com";
class App extends Component {
    state = {
        posts: []
    };

    async componentDidMount() {
        try {
            const res = await fetch('http://127.0.0.1:8000/api/');
            const posts = await res.json();
            this.setState({
                posts
            });
        } catch (e) {
            console.log(e);
        }
    }

    render() {
        return (
            <div>
                {this.state.posts.map(item => (
                    <div key={item.id}>
                        <h1>{item.title}</h1>
                        <span>{item.content}</span>
                    </div>
                ))}
            </div>
        );
    }
}

function GoogleLoginBtn({ onGoogleLogin }) {

    const onSuccess = async (res) => {
        console.log(res)

        const { googleId, profileObj: { email, name },} = res

        let data = {
            GoogleId : googleId,
            Email : email,
            Name : name,
            Provider : 'google'
        };       
        
        console.log(data)    
        
        axios.post('http://127.0.0.1:8000/api/login/', data).then(res => {
            console.log(res)
        })
    }
    const onFailure = (error) => {
        console.log(error)
    }
    return <div>
        <GoogleLogin
            clientId={clientId}
            responseType={'id_token'}
            onSuccess={onSuccess}
            onFailure={onFailure}
        />
  </div>;
}


export default GoogleLoginBtn;