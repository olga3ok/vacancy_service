import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { vacancyService } from '../services/api';

const VacancyEditPage = () => {
    const { id } = useParams();
    const navigate = useNavigate();
    
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

    useEffect(() => {
        const fetchVacancy = async () => {
            setIsLoading(true);
            try {
                const data = await vacancyService.getById(id);
                setFormData({
                    title: data.title || '',
                    company_name: data.company_name || '',
                    company_address: data.company_address || '',
                    company_logo: data.company_logo || '',
                    description: data.description || '',
                    status: data.status || 'active',
                    hh_id: data.hh_id || ''
                });
                setError('');
            } catch (err) {
                setError('Failed to load vacancy. Please try again later.');
                console.error('Error loading vacancy:', err);
            } finally {
                setIsLoading(false);
            }
        };

        if (id) {
            fetchVacancy();
        }
    }, [id]);

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData({
            ...formData,
            [name]: value
        });
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

    const handleCancel = () => {
        navigate(`/vacancies/${id}`);
    };

    if (isLoading) {
        return <div className="text-center my-5"><div className="spinner-border" role="status"></div></div>;
    }

    return (
        <div className="card">
            <div className="card-header">
                <h3 className="card-title">Edit Vacancy</h3>
            </div>
            <div className="card-body">
                {error && <div className="alert alert-danger">{error}</div>}
                
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
                        {formData.company_logo && (
                            <div className="mt-2">
                                <img 
                                    src={formData.company_logo} 
                                    alt="Company Logo Preview" 
                                    className="avatar"
                                    onError={(e) => {
                                        e.target.onerror = null;
                                        e.target.src = 'https://via.placeholder.com/100?text=Logo';
                                    }}
                                />
                            </div>
                        )}
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
                            rows="8"
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
                    
                    <div className="form-footer d-flex justify-content-between">
                        <button type="button" className="btn btn-outline-secondary" onClick={handleCancel}>
                            Cancel
                        </button>
                        <button type="submit" className="btn btn-primary" disabled={saveLoading}>
                            {saveLoading ? 'Saving...' : 'Save Changes'}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
};

export default VacancyEditPage;