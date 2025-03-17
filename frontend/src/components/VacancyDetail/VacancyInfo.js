import React from 'react';
import StatusBadge from '../common/StatusBadge';
import { formatDateTime } from '../../utils/dateFormatter';
import CompanyLogo from './CompanyLogo';

const VacancyInfo = ({ vacancy }) => {
    return (
        <div className="d-flex mb-4">
            {vacancy.company_logo && (
                <CompanyLogo 
                    logo={vacancy.company_logo} 
                    companyName={vacancy.company_name} 
                />
            )}
            <div>
                <h4>{vacancy.company_name}</h4>
                <p className="text-muted">{vacancy.company_address}</p>
                <StatusBadge status={vacancy.status} />
                
                <div className="mt-2">
                    <div className="text-muted">
                        <strong>Добавлено в систему:</strong> {formatDateTime(vacancy.created_at)}
                    </div>
                    {vacancy.published_at && (
                        <div className="text-muted">
                            <strong>Опубликовано на HH:</strong> {formatDateTime(vacancy.published_at)}
                        </div>
                    )}
                    {vacancy.updated_at && (
                        <div className="text-muted">
                            <strong>Обновлено:</strong> {formatDateTime(vacancy.updated_at)}
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
    );
};

export default VacancyInfo;