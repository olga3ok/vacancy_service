import { useState } from 'react';
import { vacancyService } from '../services/api';

export const useVacancyCreateForm = (navigate) => {
  // Основные данные формы для создания вакансии
  const [formData, setFormData] = useState({
    title: '',
    company_name: '',
    company_address: '',
    company_logo: '',
    description: '',
    status: 'active',
    hh_id: ''
  });

  // Состояния для управления режимом импорта с HH.ru
  const [isFromHH, setIsFromHH] = useState(false);
  const [hhId, setHhId] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  // Обработчик изменения полей формы
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  // Обработчик изменения ID вакансии HH.ru
  const handleHHIdChange = (e) => {
    setHhId(e.target.value);
  };

  // Переключатель режима импорта
  const toggleImportMode = () => {
    setIsFromHH(!isFromHH);
  };

  // Обработчик отправки формы
  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    try {
      if (isFromHH) {
        // Если выбран импорт с HH.ru, используется специальный метод API
        await vacancyService.createFromHH(hhId);
      } else {
        // Иначе создается вакансия с данными из формы
        await vacancyService.create(formData);
      }
      // После успешного создания перенаправление на главную страницу
      navigate('/');
    } catch (err) {
      // Обработка ошибок API
      setError(err.response?.data?.detail || 'Failed to create vacancy');
      console.error('Error creating vacancy:', err);
    } finally {
      setIsLoading(false);
    }
  };

  return {
    formData,
    isFromHH,
    hhId,
    isLoading,
    error,
    handleInputChange,
    handleHHIdChange,
    toggleImportMode,
    handleSubmit
  };
};