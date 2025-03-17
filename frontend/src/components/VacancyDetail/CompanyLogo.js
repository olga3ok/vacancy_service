import React from 'react';

const CompanyLogo = ({ logo, companyName }) => (
    <div className="me-3">
        <img 
            src={logo} 
            alt={companyName} 
            className="avatar avatar-lg"
            onError={(e) => {
                e.target.onerror = null;
                e.target.src = 'https://via.placeholder.com/100?text=Logo';
            }}
        />
    </div>
);

export default CompanyLogo;