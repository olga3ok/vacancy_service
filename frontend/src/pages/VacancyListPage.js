import React from 'react';
import { Link } from 'react-router-dom';
import SearchBar from '../components/common/SearchBar';
import VacancyTable from '../components/VacancyList/VacancyTable';
import LoadingSpinner from '../components/common/LoadingSpinner';
import ErrorAlert from '../components/common/alerts/ErrorAlert';
import EmptyState from '../components/common/EmptyState';
import { useVacancies } from '../hooks/useVacancies';
import { useSort } from '../hooks/useSort';
import { useSearch } from '../hooks/useSearch';

const VacancyListPage = () => {
    const { vacancies, isLoading, error, deleteVacancy } = useVacancies();
    const { sortConfig, handleSort, sortItems } = useSort();
    const { searchTerm, handleSearch, searchItems } = useSearch(vacancies, ['title', 'company_name']);

    if (isLoading) return <LoadingSpinner />;

    // Применяем фильтрацию поиска, затем сортировку
    const filteredVacancies = searchItems(vacancies);
    const displayVacancies = sortItems(filteredVacancies, sortConfig.key);

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
                <ErrorAlert message={error} />
                <SearchBar value={searchTerm} onChange={handleSearch} />
                
                {displayVacancies.length === 0 ? (
                    <EmptyState message="No vacancies found." />
                ) : (
                    <VacancyTable 
                        vacancies={displayVacancies}
                        sortConfig={sortConfig}
                        onSort={handleSort}
                        onDelete={deleteVacancy}
                    />
                )}
            </div>
        </div>
    );        
};

export default VacancyListPage;