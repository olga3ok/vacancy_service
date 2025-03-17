import React from 'react';

const SortableHeader = ({ title, sortKey, currentSort, onSort }) => {
  const getSortIcon = () => {
    if (currentSort.key !== sortKey) return '';
    return currentSort.direction === 'asc' ? '↑' : '↓';
  };

  return (
    <th onClick={() => onSort(sortKey)} style={{ cursor: 'pointer' }}>
      {title} {getSortIcon()}
    </th>
  );
};

export default SortableHeader;