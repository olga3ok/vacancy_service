import React from 'react';

const SuccessAlert = ({ message }) => (
    <div className="alert alert-success" role="alert">
        {message}
    </div>
);

export default SuccessAlert;