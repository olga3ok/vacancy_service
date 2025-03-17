import React from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useVacancyForm } from '../hooks/useVacancyForm';
import LoadingSpinner from '../components/common/LoadingSpinner';
import ErrorAlert from '../components/common/alerts/ErrorAlert';
import VacancyForm from '../components/common/VacancyForm/VacancyForm';

const VacancyEditPage = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  
  const {
    formData,
    initialEmptyFields,
    isLoading,
    error,
    saveLoading,
    handleInputChange,
    handleSubmit,
    handleCancel
  } = useVacancyForm(id, navigate);

  if (isLoading) return <LoadingSpinner />;

  return (
    <div className="card">
      <div className="card-header">
        <h3 className="card-title">Edit Vacancy</h3>
      </div>
      <div className="card-body">
        <ErrorAlert message={error} />
        
        <VacancyForm 
          formData={formData}
          initialEmptyFields={initialEmptyFields}
          onChange={handleInputChange}
          onSubmit={handleSubmit}
          onCancel={handleCancel}
          isSaving={saveLoading}
        />
      </div>
    </div>
  );
};

export default VacancyEditPage;