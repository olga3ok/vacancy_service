import React from 'react';
import FormField from './FormField';
import LogoPreview from './LogoPreview';
import FormActions from './FormActions';

const statusOptions = [
  { value: 'active', label: 'Active' },
  { value: 'closed', label: 'Closed' },
  { value: 'draft', label: 'Draft' }
];

const VacancyForm = ({ 
  formData, 
  initialEmptyFields = {}, 
  onChange, 
  onSubmit, 
  onCancel, 
  isSaving,
  submitButtonText = 'Save Changes',
  showCancelButton = true
}) => {
  return (
    <form onSubmit={onSubmit}>
      <FormField 
        label="Title"
        name="title"
        value={formData.title}
        onChange={onChange}
        required={!initialEmptyFields.title}
      />
      
      <FormField 
        label="Company Name"
        name="company_name"
        value={formData.company_name}
        onChange={onChange}
        required={!initialEmptyFields.company_name}
      />
      
      <FormField 
        label="Company Address"
        name="company_address"
        value={formData.company_address}
        onChange={onChange}
        required={!initialEmptyFields.company_address}
      />
      
      <FormField 
        label="Company Logo URL"
        name="company_logo"
        value={formData.company_logo}
        onChange={onChange}
        required={!initialEmptyFields.company_logo}
      >
        <LogoPreview logoUrl={formData.company_logo} />
      </FormField>
      
      <FormField 
        label="Status"
        name="status"
        value={formData.status}
        onChange={onChange}
        required={true}
        type="select"
        options={statusOptions}
      />
      
      <FormField 
        label="Description"
        name="description"
        value={formData.description}
        onChange={onChange}
        required={!initialEmptyFields.description}
        type="textarea"
        rows={5}
      />
      
      <FormField 
        label="HH.ru ID (optional)"
        name="hh_id"
        value={formData.hh_id}
        onChange={onChange}
        required={false}
      />
      
      {showCancelButton ? (
        <FormActions onCancel={onCancel} isSaving={isSaving} submitText={submitButtonText} />
      ) : (
        <div className="form-footer">
          <button type="submit" className="btn btn-primary" disabled={isSaving}>
            {submitButtonText}
          </button>
        </div>
      )}
    </form>
  );
};

export default VacancyForm;