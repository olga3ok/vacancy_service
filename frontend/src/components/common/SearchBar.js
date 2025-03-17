import React from 'react';

const SearchBar = ({ value, onChange }) => (
  <div className="mb-3">
    <div className="input-group">
      <span className="input-group-text">
        <svg xmlns="http://www.w3.org/2000/svg" className="icon" width="24" height="24" viewBox="0 0 24 24" strokeWidth="2" stroke="currentColor" fill="none" strokeLinecap="round" strokeLinejoin="round">
          <path stroke="none" d="M0 0h24v24H0z" fill="none" />
          <circle cx="10" cy="10" r="7" />
          <line x1="21" y1="21" x2="15" y2="15" />
        </svg>
      </span>
      <input 
        type="text" 
        className="form-control" 
        placeholder="Search vacancies..." 
        value={value}
        onChange={onChange}
      />
    </div>
  </div>
);

export default SearchBar;