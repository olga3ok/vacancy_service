import React from 'react';

const FormActions = ({ onCancel, isSaving, submitText = 'Save Changes' }) => (
  <div className="form-footer d-flex justify-content-between">
    <button type="button" className="btn btn-outline-secondary" onClick={onCancel}>
      Cancel
    </button>
    <button type="submit" className="btn btn-primary" disabled={isSaving}>
      {submitText}
    </button>
  </div>
);

export default FormActions;