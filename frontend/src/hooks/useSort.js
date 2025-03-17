import { useState } from 'react';

export const useSort = () => {
  const [sortConfig, setSortConfig] = useState({ key: null, direction: 'asc' });
  
  const handleSort = (key) => {
    const direction = sortConfig.key === key && sortConfig.direction === 'asc' 
      ? 'desc' 
      : 'asc';
    setSortConfig({ key, direction });
  };
  
  const sortItems = (items, sortKey) => {
    if (!sortConfig.key) return items;
    
    return [...items].sort((a, b) => {
      const compareMap = {
        'title': () => sortValueCompare(a.title, b.title),
        'company': () => sortValueCompare(a.company_name, b.company_name),
        'status': () => sortValueCompare(a.status, b.status)
      };
      
      const compare = compareMap[sortConfig.key] || (() => 0);
      return compare();
    });
  };
  
  const sortValueCompare = (a, b) => {
    return sortConfig.direction === 'asc'
      ? String(a).localeCompare(String(b))
      : String(b).localeCompare(String(a));
  };
  
  return {
    sortConfig,
    handleSort,
    sortItems
  };
};