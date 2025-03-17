import React from 'react';
import SortableHeader from './SortableHeader';
import VacancyRow from './VacancyRow';

const VacancyTable = ({ vacancies, sortConfig, onSort, onDelete }) => (
  <div className="table-responsive">
    <table className="table table-vcenter card-table">
      <thead>
        <tr>
          <SortableHeader 
            title="Title" 
            sortKey="title" 
            currentSort={sortConfig} 
            onSort={onSort} 
          />
          <SortableHeader 
            title="Company" 
            sortKey="company" 
            currentSort={sortConfig} 
            onSort={onSort} 
          />
          <SortableHeader 
            title="Status" 
            sortKey="status" 
            currentSort={sortConfig} 
            onSort={onSort} 
          />
          <th className="w-1"></th>
        </tr>
      </thead>
      <tbody>
        {vacancies.map(vacancy => (
          <VacancyRow 
            key={vacancy.id} 
            vacancy={vacancy} 
            onDelete={onDelete} 
          />
        ))}
      </tbody>
    </table>
  </div>
);

export default VacancyTable;