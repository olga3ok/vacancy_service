import React from 'react';

const RefreshButton = ({ refreshLoading, handleRefreshFromHH }) => (
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
);

export default RefreshButton;