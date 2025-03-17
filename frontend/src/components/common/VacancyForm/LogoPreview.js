import React from 'react';

const LogoPreview = ({ logoUrl }) => {
    if (!logoUrl) return null;
    
    return (
      <div className="mt-2">
        <img 
          src={logoUrl} 
          alt="Company Logo Preview" 
          className="avatar"
          onError={(e) => {
            e.target.onerror = null;
            e.target.src = 'https://via.placeholder.com/100?text=Logo';
          }}
        />
      </div>
    );
  };
  
export default LogoPreview;