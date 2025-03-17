import React from 'react';

const FormToggle = ({ isFromHH, onToggle }) => {
  return (
    <div className="form-check mb-3">
      <input
        className="form-check-input"
        type="checkbox"
        id="fromHH"
        checked={isFromHH}
        onChange={onToggle}
      />
      <label className="form-check-label" htmlFor="fromHH">
        Import from HH.ru
      </label>
    </div>
  );
};

export default FormToggle;