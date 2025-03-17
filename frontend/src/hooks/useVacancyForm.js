import { useState, useEffect } from 'react';
import { vacancyService } from '../services/api';

export const useVacancyForm = (id, navigate) => {
  const [initialEmptyFields, setInitialEmptyFields] = useState({
    title: false,
    company_name: false,
    company_address: false,
    company_logo: false,
    description: false,
    hh_id: true
  });
  
  const [formData, setFormData] = useState({
    title: '',
    company_name: '',
    company_address: '',
    company_logo: '',
    description: '',
    status: 'active',
    hh_id: ''
  });

  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');
  const [saveLoading, setSaveLoading] = useState(false);

  // Загрузка данных вакансии
  useEffect(() => {
    const fetchVacancy = async () => {
      if (!id) return;
      
      setIsLoading(true);
      
      try {
        const data = await vacancyService.getById(id);
        
        // Определение пустых полей
        const emptyFields = {
          title: !data.title,
          company_name: !data.company_name,
          company_address: !data.company_address,
          company_logo: !data.company_logo,
          description: !data.description,
          hh_id: true
        };
        
        setInitialEmptyFields(emptyFields);
        
        // Заполнение формы данными
        setFormData({
          title: data.title || '',
          company_name: data.company_name || '',
          company_address: data.company_address || '',
          company_logo: data.company_logo || '',
          description: data.description || '',
          status: data.status || 'active',
          hh_id: data.hh_id || ''
        });
      } catch (err) {
        setError('Failed to load vacancy. Please try again later.');
        console.error('Error loading vacancy:', err);
      } finally {
        setIsLoading(false);
      }
    };

    fetchVacancy();
  }, [id]);

  // Обработчики событий
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSaveLoading(true);

    try {
      await vacancyService.update(id, formData);
      navigate(`/vacancies/${id}`);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to update vacancy');
      console.error('Error updating vacancy:', err);
    } finally {
      setSaveLoading(false);
    }
  };

  const handleCancel = () => navigate(`/vacancies/${id}`);

  return {
    formData,
    initialEmptyFields,
    isLoading,
    error,
    saveLoading,
    handleInputChange,
    handleSubmit,
    handleCancel
  };
};