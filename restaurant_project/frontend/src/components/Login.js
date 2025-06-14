import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import axios from 'axios';
import { GoogleLogin } from '@react-oauth/google';
import './AuthForm.css';

function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  // Handle normal username/password login
  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const res = await axios.post('http://localhost:8000/accounts/login/', {
        username, password
      }, { withCredentials: true });

      if (res.status === 200) {
        navigate('/dashboard');
      }
    } catch {
      alert('Login failed');
    }
  };

  // Handle Google OAuth login
  const handleGoogleSuccess = async (credentialResponse) => {
    try {
      const res = await axios.post('http://localhost:8000/accounts/oauth/', {
        token: credentialResponse.credential
      }, { withCredentials: true });

      if (res.status === 200) {
        navigate('/dashboard');
      }
    } catch {
      alert("Google login failed");
    }
  };

  return (
    <div className="login-container">
      <form className="login-card" onSubmit={handleLogin}>
        <h2 className="login-title">Login</h2>

        <label>Email address</label>
        <input
          type="email"
          placeholder="Enter email"
          value={username}
          onChange={e => setUsername(e.target.value)}
        />

        <label>Password</label>
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={e => setPassword(e.target.value)}
        />

        <button type="submit" className="login-button">Login</button>

        <p className="signup-link">
          Don’t have an account? <Link to="/signup">Signup here</Link>
        </p>

        <div style={{ marginTop: '20px' }}>
          <p>Or login with Google</p>
          <GoogleLogin
            onSuccess={handleGoogleSuccess}
            onError={() => alert('Google login error')}
          />
        </div>
      </form>
    </div>
  );
}

export default Login;

