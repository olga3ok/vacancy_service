import React from 'react';

const ErrorAlert = ({ message }) => (
  message ? <div className="alert alert-danger">{message}</div> : null
);

export default ErrorAlert;