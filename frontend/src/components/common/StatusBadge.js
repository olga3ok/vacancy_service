import React from 'react';

const StatusBadge = ({ status }) => {
    const getStatusBadge = (status) => {
        switch (status) {
            case 'active':
                return <span className="badge bg-success">Active</span>;
            case 'closed':
                return <span className="badge bg-danger">Closed</span>;
            case 'draft':
                return <span className="badge bg-light">Draft</span>;
            case 'outdated':
                return <span className="badge bg-light">Outdated</span>;
            default:
                return <span className="badge bg-light">Unknown</span>;
        }
    };
    
    return getStatusBadge(status);
};

export default StatusBadge;