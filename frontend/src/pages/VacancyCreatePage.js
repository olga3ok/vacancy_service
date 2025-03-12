import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { vacancyService } from '../services/api';

const VacancyCreatePage = () => {
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

    const navigate = useNavigate();

    // Обработчик изменения полей формы
    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData({
            ...formData,
            [name]: value
        });
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

    return (
        <div className="card">
          <div className="card-header">
            <h3 className="card-title">Create New Vacancy</h3>
          </div>
          <div className="card-body">
            {error && <div className="alert alert-danger">{error}</div>}
            
            {/* Переключатель между ручным созданием и импортом с HH.ru */}
            <div className="form-check mb-3">
              <input
                className="form-check-input"
                type="checkbox"
                id="fromHH"
                checked={isFromHH}
                onChange={() => setIsFromHH(!isFromHH)}
              />
              <label className="form-check-label" htmlFor="fromHH">
                Import from HH.ru
              </label>
            </div>
            
            {isFromHH ? (
              // Форма для импорта с HH.ru
              <form onSubmit={handleSubmit}>
                <div className="mb-3">
                  <label className="form-label">HH.ru Vacancy ID</label>
                  <input
                    type="text"
                    className="form-control"
                    value={hhId}
                    onChange={(e) => setHhId(e.target.value)}
                    required
                  />
                </div>
                <div className="form-footer">
                  <button type="submit" className="btn btn-primary" disabled={isLoading}>
                    {isLoading ? 'Importing...' : 'Import from HH.ru'}
                  </button>
                </div>
              </form>
            ) : (
              // Форма для ручного создания вакансии
              <form onSubmit={handleSubmit}>
                <div className="mb-3">
                  <label className="form-label">Title</label>
                  <input
                    type="text"
                    className="form-control"
                    name="title"
                    value={formData.title}
                    onChange={handleInputChange}
                    required
                  />
                </div>
                
                <div className="mb-3">
                  <label className="form-label">Company Name</label>
                  <input
                    type="text"
                    className="form-control"
                    name="company_name"
                    value={formData.company_name}
                    onChange={handleInputChange}
                    required
                  />
                </div>
                
                <div className="mb-3">
                  <label className="form-label">Company Address</label>
                  <input
                    type="text"
                    className="form-control"
                    name="company_address"
                    value={formData.company_address}
                    onChange={handleInputChange}
                    required
                  />
                </div>
                
                <div className="mb-3">
                  <label className="form-label">Company Logo URL</label>
                  <input
                    type="text"
                    className="form-control"
                    name="company_logo"
                    value={formData.company_logo}
                    onChange={handleInputChange}
                    required
                  />
                </div>
                
                <div className="mb-3">
                  <label className="form-label">Status</label>
                  <select
                    className="form-select"
                    name="status"
                    value={formData.status}
                    onChange={handleInputChange}
                    required
                  >
                    <option value="active">Active</option>
                    <option value="closed">Closed</option>
                    <option value="draft">Draft</option>
                  </select>
                </div>
                
                <div className="mb-3">
                  <label className="form-label">Description</label>
                  <textarea
                    className="form-control"
                    name="description"
                    rows="5"
                    value={formData.description}
                    onChange={handleInputChange}
                    required
                  ></textarea>
                </div>
                
                <div className="mb-3">
                  <label className="form-label">HH.ru ID (optional)</label>
                  <input
                    type="text"
                    className="form-control"
                    name="hh_id"
                    value={formData.hh_id}
                    onChange={handleInputChange}
                  />
                </div>
                
                <div className="form-footer">
                  <button type="submit" className="btn btn-primary" disabled={isLoading}>
                    {isLoading ? 'Creating...' : 'Create Vacancy'}
                  </button>
                </div>
              </form>
            )}
          </div>
        </div>
    );
}

export default VacancyCreatePage;