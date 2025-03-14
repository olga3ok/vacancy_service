import React, { useState, useEffect } from 'react';
import { Link, useParams, useNavigate } from 'react-router-dom';
import { vacancyService } from '../services/api';

const VacancyDetailPage = () => {
    const [vacancy, setVacancy] = useState(null);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState('');
    const [refreshLoading, setRefreshLoading] = useState(false);
    const [refreshSuccess, setRefreshSuccess] = useState(false);

    const { id } = useParams();
    const navigate = useNavigate();

    const fetchVacancy = async () => {
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
    };

    useEffect(() => {
        if (id) {
            fetchVacancy();
        }
    }, [id]);

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
            await fetchVacancy(); // Перезагрузка данных о вакансии
            setRefreshSuccess(true);
            setTimeout(() => setRefreshSuccess(false), 3000);
        } catch (err) {
            setError(err.response?.data?.detail || 'Не удалось обновить данные с HH.ru');
            console.error('Ошибка при обновлении данных с HH.ru', err);
        } finally {
            setRefreshLoading(false);
        }
    };

    const renderStatus = (status) => {
        switch (status) {
            case 'active':
                return <span className="badge bg-success">Active</span>;
            case 'closed':
                return <span className="badge bg-danger">Closed</span>;
            case 'draft':
                return <span className="badge bg-secondary">Draft</span>;
            default:
                return <span className="badge bg-light">Unknown</span>;
        }
    };

    // Форматирование даты и времени
    const formatDateTime = (dateString) => {
        if (!dateString) return 'Не указано';
        
        const date = new Date(dateString);
        return date.toLocaleString('ru-RU', {
            day: '2-digit',
            month: '2-digit',
            year: 'numeric',
            hour: '2-digit',
            minute: '2-digit',
            //timeZone: Intl.DateTimeFormat().resolvedOptions().timezone
        });
    };

    if (isLoading) {
        return <div className="text-center my-5"><div className="spinner-border" role="status"></div></div>;
    }

    if (error) {
        return <div className="alert alert-danger">{error}</div>;
    }

    if (!vacancy) {
        return <div className="alert alert-warning">Vacancy not found.</div>;
    }

    return (
        <div className="card">
            <div className="card-header">
                <div className="d-flex justify-content-between align-items-center w-100">
                    <h3 className="card-title">{vacancy.title}</h3>
                    <div className="btn-group">
                    {vacancy.hh_id && (
                            <button 
                                className="btn btn-info" 
                                onClick={handleRefreshFromHH}
                                disabled={refreshLoading}
                            >
                                {refreshLoading ? (
                                    <>
                                        <span className="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                                        Обновление...
                                    </>
                                ) : (
                                    <>
                                        <svg xmlns="http://www.w3.org/2000/svg" className="icon me-1" width="24" height="24" viewBox="0 0 24 24" strokeWidth="2" stroke="currentColor" fill="none" strokeLinecap="round" strokeLinejoin="round">
                                            <path stroke="none" d="M0 0h24v24H0z" fill="none" />
                                            <path d="M20 11a8.1 8.1 0 0 0 -15.5 -2m-.5 -4v4h4" />
                                            <path d="M4 13a8.1 8.1 0 0 0 15.5 2m.5 4v-4h-4" />
                                        </svg>
                                        Обновить с HH.ru
                                    </>
                                )}
                            </button>
                        )}
                        <Link to={`/vacancies/${id}/edit`} className="btn btn-primary">
                            <svg xmlns="http://www.w3.org/2000/svg" className="icon" width="24" height="24" viewBox="0 0 24 24" strokeWidth="2" stroke="currentColor" fill="none" strokeLinecap="round" strokeLinejoin="round">
                                <path stroke="none" d="M0 0h24v24H0z" fill="none" />
                                <path d="M4 20h4l10.5 -10.5a1.5 1.5 0 0 0 -4 -4l-10.5 10.5v4" />
                                <line x1="13.5" y1="6.5" x2="17.5" y2="10.5" />
                            </svg>
                            Edit
                        </Link>
                        <button className="btn btn-danger" onClick={handleDelete}>
                            <svg xmlns="http://www.w3.org/2000/svg" className="icon" width="24" height="24" viewBox="0 0 24 24" strokeWidth="2" stroke="currentColor" fill="none" strokeLinecap="round" strokeLinejoin="round">
                                <path stroke="none" d="M0 0h24v24H0z" fill="none" />
                                <line x1="4" y1="7" x2="20" y2="7" />
                                <line x1="10" y1="11" x2="10" y2="17" />
                                <line x1="14" y1="11" x2="14" y2="17" />
                                <path d="M5 7l1 12a2 2 0 0 0 2 2h8a2 2 0 0 0 2 -2l1 -12" />
                                <path d="M9 7v-3a1 1 0 0 1 1 -1h4a1 1 0 0 1 1 1v3" />
                            </svg>
                            Delete
                        </button>
                    </div>
                </div>
            </div>

            <div className="card-body">
                <div className="d-flex mb-4">
                    {vacancy.company_logo && (
                        <div className="me-3">
                            <img 
                                src={vacancy.company_logo} 
                                alt={vacancy.company_name} 
                                className="avatar avatar-lg"
                                onError={(e) => {
                                    e.target.onerror = null;
                                    e.target.src = 'https://via.placeholder.com/100?text=Logo';
                                }}
                            />
                        </div>
                    )}
                    <div>
                        <h4>{vacancy.company_name}</h4>
                        <p className="text-muted">{vacancy.company_address}</p>
                        <div>{renderStatus(vacancy.status)}</div>
                        
                        {/* Информация о датах */}
                        <div className="mt-2">
                            <div className="text-muted">
                                <strong>Добавлено в систему:</strong> {formatDateTime(vacancy.created_at)}
                            </div>
                            {vacancy.published_at && (
                                <div className="text-muted">
                                    <strong>Опубликовано на HH:</strong> {formatDateTime(vacancy.published_at)}
                                </div>
                            )}
                        </div>
                        
                        {vacancy.hh_id && (
                            <div className="mt-2">
                                <a 
                                    href={`https://hh.ru/vacancy/${vacancy.hh_id}`} 
                                    target="_blank" 
                                    rel="noopener noreferrer"
                                    className="btn btn-sm btn-outline-secondary"
                                >
                                    View on HH.ru
                                </a>
                            </div>
                        )}
                    </div>
                </div>
                
                <h4>Description</h4>
                <div className="vacancy-description mt-3 mb-4"
                dangerouslySetInnerHTML={{ __html: vacancy.description }}>
                </div>
                
                <div className="d-flex justify-content-between mt-4">
                    <Link to="/" className="btn btn-outline-secondary">
                        Back to List
                    </Link>
                </div>
            </div>
        </div>
    );
};

export default VacancyDetailPage;