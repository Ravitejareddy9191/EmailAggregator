import React from 'react';
import { createRoot } from 'react-dom/client';
import App from './App';
import './App.css';
import { GoogleOAuthProvider } from '@react-oauth/google';

const clientId = "361799545263-b016bsotf6jmijjbqab3pjlha68g9ap7.apps.googleusercontent.com";

const root = createRoot(document.getElementById('root'));
root.render(
  <GoogleOAuthProvider clientId={clientId}>
    <App />
  </GoogleOAuthProvider>
);
