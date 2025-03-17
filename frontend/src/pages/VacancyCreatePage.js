import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useVacancyCreateForm } from '../hooks/useVacancyCreateForm';
import ErrorAlert from '../components/common/alerts/ErrorAlert';
import VacancyForm from '../components/common/VacancyForm/VacancyForm';
import ImportHHForm from '../components/VacancyCreate/ImportHHForm';
import FormToggle from '../components/VacancyCreate/FormToggle';

const VacancyCreatePage = () => {
  const navigate = useNavigate();
  
  const {
    formData,
    isFromHH,
    hhId,
    isLoading,
    error,
    handleInputChange,
    handleHHIdChange,
    toggleImportMode,
    handleSubmit
  } = useVacancyCreateForm(navigate);

  return (
    <div className="card">
      <div className="card-header">
        <h3 className="card-title">Create New Vacancy</h3>
      </div>
      <div className="card-body">
        <ErrorAlert message={error} />
        
        <FormToggle 
          isFromHH={isFromHH}
          onToggle={toggleImportMode}
        />
        
        {isFromHH ? (
          <ImportHHForm 
            hhId={hhId}
            onChange={handleHHIdChange}
            onSubmit={handleSubmit}
            isLoading={isLoading}
          />
        ) : (
          <VacancyForm 
            formData={formData}
            initialEmptyFields={{}}
            onChange={handleInputChange}
            onSubmit={handleSubmit}
            isSaving={isLoading}
            submitButtonText={isLoading ? 'Creating...' : 'Create Vacancy'}
            showCancelButton={false}
          />
        )}
      </div>
    </div>
  );
};

export default VacancyCreatePage;