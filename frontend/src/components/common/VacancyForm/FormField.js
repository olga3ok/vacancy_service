import React from 'react';

const FormField = ({ label, name, value, onChange, required, type = 'text', rows, children, options }) => {
  const isTextarea = type === 'textarea';
  const isSelect = type === 'select';
  
  return (
    <div className="mb-3">
      <label className="form-label">
        {label}
        {required && <span className="text-danger ms-1">*</span>}
      </label>
      
      {isTextarea ? (
        <textarea
          className="form-control"
          name={name}
          rows={rows || 8}
          value={value}
          onChange={onChange}
          required={required}
        />
      ) : isSelect ? (
        <select
          className="form-select"
          name={name}
          value={value}
          onChange={onChange}
          required={required}
        >
          {options.map(option => (
            <option key={option.value} value={option.value}>
              {option.label}
            </option>
          ))}
        </select>
      ) : (
        <input
          type={type}
          className="form-control"
          name={name}
          value={value}
          onChange={onChange}
          required={required}
        />
      )}
      
      {children}
    </div>
  );
};

export default FormField;