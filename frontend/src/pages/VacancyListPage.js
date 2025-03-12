import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { vacancyService } from '../services/api';

const VacancyListPage = () => {
    const [vacancies, setVacancies] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState(null);
    const [searchTerm, setSearchTerm] = useState('');

    useEffect(() => {
        loadVacancies();
    }, []);

    const loadVacancies = async () => {
        setIsLoading(true);
        try {
            const data = await vacancyService.getAll();
            setVacancies(data);
            setError('');
        } catch (err) {
            setError('Failed to load vacancies. Please try again later.');
            console.error('Error loading vacancies:', err);
        } finally {
            setIsLoading(false);
        }
    };

    const handleDelete = async (id) => {
        if (window.confirm('Are you sure you want to delete this vacancy?')) {
            try {
                await vacancyService.delete(id);
                loadVacancies();
            } catch (err) {
                setError('Failed to delete vacancy.');
                console.error('Error deleting vacancy:', err);
            }
        }
    };

    const handleSearch = (e) => {
        setSearchTerm(e.target.value);
    };

    const filteredVacancies = vacancies.filter(vacancy =>
        vacancy.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
        vacancy.company_name.toLowerCase().includes(searchTerm.toLocaleLowerCase())
    );

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

    if (isLoading) {
        return <div className="text-center my-5"><div className="spinner-border" role="status"></div></div>;
    }

    return (
        <div className="card">
            <div className="card-header">
            <div className="d-flex justify-content-between align-items-center w-100">
                <h3 className="card-title">All Vacancies</h3>
                <Link to="/vacancies/create" className="btn btn-primary">
                    <svg xmlns="http://www.w3.org/2000/svg" className="icon" width="24" height="24" viewBox="0 0 24 24" strokeWidth="2" stroke="currentColor" fill="none" strokeLinecap="round" strokeLinejoin="round">
                        <path stroke="none" d="M0 0h24v24H0z" fill="none" />
                        <line x1="12" y1="5" x2="12" y2="19" />
                        <line x1="5" y1="12" x2="19" y2="12" />
                    </svg>
                    Create New
                </Link>
            </div>
            </div>
            <div className="card-body">
                {error && <div className="alert alert-danger">{error}</div>}
                
                <div className="mb-3">
                    <div className="input-group">
                        <span className="input-group-text">
                            <svg xmlns="http://www.w3.org/2000/svg" className="icon" width="24" height="24" viewBox="0 0 24 24" strokeWidth="2" stroke="currentColor" fill="none" strokeLinecap="round" strokeLinejoin="round">
                                <path stroke="none" d="M0 0h24v24H0z" fill="none" />
                                <circle cx="10" cy="10" r="7" />
                                <line x1="21" y1="21" x2="15" y2="15" />
                            </svg>
                        </span>
                        <input 
                            type="text" 
                            className="form-control" 
                            placeholder="Search vacancies..." 
                            value={searchTerm}
                            onChange={handleSearch}
                        />
                    </div>
                </div>
                
                {filteredVacancies.length === 0 ? (
                    <div className="text-center py-5">
                        <p className="text-muted">No vacancies found.</p>
                    </div>
                ) : (
                    <div className="table-responsive">
                        <table className="table table-vcenter card-table">
                            <thead>
                                <tr>
                                    <th>Title</th>
                                    <th>Company</th>
                                    <th>Status</th>
                                    <th className="w-1"></th>
                                </tr>
                            </thead>
                            <tbody>
                                {filteredVacancies.map(vacancy => (
                                    <tr key={vacancy.id}>
                                        <td>
                                            <Link to={`/vacancies/${vacancy.id}`} className="text-reset">
                                                {vacancy.title}
                                            </Link>
                                        </td>
                                        <td className="text-muted">
                                            {vacancy.company_name}
                                        </td>
                                        <td>
                                            {renderStatus(vacancy.status)}
                                        </td>
                                        <td>
                                            <div className="btn-group">
                                                <Link to={`/vacancies/${vacancy.id}`} className="btn btn-sm btn-outline-primary">
                                                    View
                                                </Link>
                                                <Link to={`/vacancies/${vacancy.id}/edit`} className="btn btn-sm btn-outline-secondary">
                                                    Edit
                                                </Link>
                                                <button 
                                                    className="btn btn-sm btn-outline-danger"
                                                    onClick={() => handleDelete(vacancy.id)}
                                                >
                                                    Delete
                                                </button>
                                            </div>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                )}
            </div>
        </div>
    );        
};

export default VacancyListPage;