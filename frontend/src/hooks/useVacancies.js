import { useState, useEffect } from 'react';
import { vacancyService } from '../services/api';

export const useVacancies = () => {
  const [vacancies, setVacancies] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  
  const loadVacancies = async () => {
    setIsLoading(true);
    try {
      const data = await vacancyService.getAll();
      setVacancies(data.sort((a, b) => new Date(a.created_at) - new Date(b.created_at)));
      setError('');
    } catch (err) {
      setError('Failed to load vacancies. Please try again later.');
      console.error('Error loading vacancies:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const deleteVacancy = async (id) => {
    if (window.confirm('Are you sure you want to delete this vacancy?')) {
      try {
        await vacancyService.delete(id);
        await loadVacancies();
      } catch (err) {
        setError('Failed to delete vacancy.');
        console.error('Error deleting vacancy:', err);
      }
    }
  };

  useEffect(() => {
    loadVacancies();
  }, []);

  return {
    vacancies,
    isLoading,
    error,
    deleteVacancy
  };
};