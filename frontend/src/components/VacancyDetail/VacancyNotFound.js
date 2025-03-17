import React from 'react';
import { Link } from 'react-router-dom';

const VacancyNotFound = () => (
    <div className="alert alert-warning">
        Vacancy not found.
        <div className="mt-3">
            <Link to="/" className="btn btn-outline-secondary">
                Back to List
            </Link>
        </div>
    </div>
);

export default VacancyNotFound;