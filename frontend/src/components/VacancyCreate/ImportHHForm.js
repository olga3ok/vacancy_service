import React from 'react';

const ImportHHForm = ({ hhId, onChange, onSubmit, isLoading }) => {
  return (
    <form onSubmit={onSubmit}>
      <div className="mb-3">
        <label className="form-label">HH.ru Vacancy ID</label>
        <input
          type="text"
          className="form-control"
          value={hhId}
          onChange={onChange}
          required
        />
      </div>
      <div className="form-footer">
        <button type="submit" className="btn btn-primary" disabled={isLoading}>
          {isLoading ? 'Importing...' : 'Import from HH.ru'}
        </button>
      </div>
    </form>
  );
};

export default ImportHHForm;