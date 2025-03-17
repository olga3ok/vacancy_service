import React, { useState, useEffect, useCallback } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { vacancyService } from '../services/api';
import LoadingSpinner from '../components/common/LoadingSpinner';
import ErrorAlert from '../components/common/alerts/ErrorAlert';
import VacancyNotFound from '../components/VacancyDetail//VacancyNotFound';
import VacancyHeader from '../components/VacancyDetail//VacancyHeader';
import VacancyInfo from '../components/VacancyDetail/VacancyInfo';
import SuccessAlert from '../components/common/alerts/SuccessAlert';

const VacancyDetailPage = () => {
    const [vacancy, setVacancy] = useState(null);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState('');
    const [refreshLoading, setRefreshLoading] = useState(false);
    const [refreshSuccess, setRefreshSuccess] = useState(false);

    const { id } = useParams();
    const navigate = useNavigate();

    const fetchVacancy = useCallback(async () => {
        setIsLoading(true);
        try {
            const data = await vacancyService.getById(id);
            setVacancy(data);
            setError('');
        } catch (err) {
            setError('Failed to load vacancy details. Please try again later.');
            console.error('Error loading vacancy details:', err);
        } finally {
            setIsLoading(false);
        }
    }, [id]);

    useEffect(() => {
        if (id) {
            fetchVacancy();
        }
    }, [id, fetchVacancy]);

    const handleDelete = async () => {
        if (window.confirm('Are you sure you want to delete this vacancy?')) {
            try {
                await vacancyService.delete(id);
                navigate('/');
            } catch (err) {
                setError('Failed to delete vacancy.');
                console.error('Error deleting vacancy:', err);
            }
        }
    };

    const handleRefreshFromHH = async () => {
        if (!vacancy.hh_id) {
            setError('Для обновления данных необходим ID вакансии на HH.ru');
            return;
        }

        setError('');
        setRefreshSuccess(false);
        setRefreshLoading(true);

        try {
            await vacancyService.refreshFromHH(id);
            await fetchVacancy();
            setRefreshSuccess(true);
            setTimeout(() => setRefreshSuccess(false), 3000);
        } catch (err) {
            setError(err.response?.data?.detail || 'Не удалось обновить данные с HH.ru');
            console.error('Ошибка при обновлении данных с HH.ru', err);
        } finally {
            setRefreshLoading(false);
        }
    };

    if (isLoading) return <LoadingSpinner />;
    if (error) return <ErrorAlert message={error} />;
    if (!vacancy) return <VacancyNotFound />;

    return (
        <div className="card">
            <VacancyHeader 
                title={vacancy.title} 
                hasHhId={!!vacancy.hh_id}
                refreshLoading={refreshLoading}
                handleRefreshFromHH={handleRefreshFromHH}
                handleDelete={handleDelete}
                id={id}
            />
            
            {refreshSuccess && <SuccessAlert message="Данные успешно обновлены с HH.ru" />}
            
            <div className="card-body">
                <VacancyInfo vacancy={vacancy} />
                
                <h4>Description</h4>
                <div className="vacancy-description mt-3 mb-4"
                    dangerouslySetInnerHTML={{ __html: vacancy.description }}>
                </div>
            </div>
        </div>
    );
};

export default VacancyDetailPage;