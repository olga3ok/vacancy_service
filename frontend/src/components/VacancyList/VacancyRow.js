import React from 'react';
import { Link } from 'react-router-dom';
import StatusBadge from '../common/StatusBadge';

const VacancyRow = ({ vacancy, onDelete }) => (
  <tr key={vacancy.id}>
    <td>
      <Link to={`/vacancies/${vacancy.id}`} className="text-reset">
        {vacancy.title}
      </Link>
    </td>
    <td className="text-muted">{vacancy.company_name}</td>
    <td><StatusBadge status={vacancy.status} /></td>
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
          onClick={() => onDelete(vacancy.id)}
        >
          Delete
        </button>
      </div>
    </td>
  </tr>
);

export default VacancyRow;