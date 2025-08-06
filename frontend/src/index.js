import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import * as Sentry from '@sentry/react';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';

Sentry.init({
  dsn: process.env.REACT_APP_SENTRY_DSN,
  tracesSampleRate: 1.0,
});

// Fix for default marker icon issue with Webpack
delete L.Icon.Default.prototype._getIconUrl;

L.Icon.Default.mergeOptions({
  iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
  iconUrl: require('leaflet/dist/images/marker-icon.png'),
  shadowUrl: require('leaflet/dist/images/marker-shadow.png'),
});

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
); 