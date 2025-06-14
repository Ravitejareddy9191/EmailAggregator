import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import axios from 'axios';
import './AuthForm.css';

function Signup() {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password1: '',
    password2: ''
  });

  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({ 
      ...formData, 
      [e.target.name]: e.target.value 
    });
  };

  const handleSignup = async (e) => {
    e.preventDefault();
    try {
      const res = await axios.post('http://localhost:8000/auth/registration/', formData);
      if (res.status === 201) {
        alert('Signup successful. Please log in.');
        navigate('/login');
      }
    } catch (error) {
      console.error("Signup error:", error.response?.data || error.message);
      alert("Signup failed: " + JSON.stringify(error.response?.data || {}));
    }
  };

  // OPTIONAL: Google OAuth (if implemented)
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
      <form className="login-card" onSubmit={handleSignup}>
        <h2 className="login-title">Signup</h2>

        <label>Username</label>
        <input
          name="username"
          placeholder="Username"
          value={formData.username}
          onChange={handleChange}
          required
        />

        <label>Email</label>
        <input
          type="email"
          name="email"
          placeholder="Enter email"
          value={formData.email}
          onChange={handleChange}
          required
        />

        <label>Password</label>
        <input
          type="password"
          name="password1"
          placeholder="Password"
          value={formData.password1}
          onChange={handleChange}
          required
        />

        <label>Confirm Password</label>
        <input
          type="password"
          name="password2"
          placeholder="Confirm Password"
          value={formData.password2}
          onChange={handleChange}
          required
        />

        <button type="submit" className="login-button">Signup</button>

        <p className="signup-link">
          Already have an account? <Link to="/login">Login here</Link>
        </p>
      </form>
    </div>
  );
}

export default Signup;
