import React from 'react';
import RefreshButton from '../common/buttons/RefreshButton';
import EditButton from '../common/buttons/EditButton';
import DeleteButton from '../common/buttons/DeleteButton';

const VacancyHeader = ({ 
    title, 
    hasHhId, 
    refreshLoading, 
    handleRefreshFromHH, 
    handleDelete, 
    id 
}) => {
    return (
        <div className="card-header">
            <div className="d-flex justify-content-between align-items-center w-100">
                <h3 className="card-title">{title}</h3>
                <div className="btn-group">
                    {hasHhId && (
                        <RefreshButton 
                            refreshLoading={refreshLoading} 
                            handleRefreshFromHH={handleRefreshFromHH} 
                        />
                    )}
                    <EditButton id={id} />
                    <DeleteButton handleDelete={handleDelete} />
                </div>
            </div>
        </div>
    );
};

export default VacancyHeader;