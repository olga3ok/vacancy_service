import { useState } from 'react';

export const useSearch = (items, searchFields = []) => {
  const [searchTerm, setSearchTerm] = useState('');
  
  const handleSearch = (e) => setSearchTerm(e.target.value);
  
  const searchItems = (items) => {
    if (!searchTerm) return items;
    
    return items.filter(item => {
      return searchFields.some(field => {
        const value = field.includes('.') 
          ? field.split('.').reduce((obj, key) => obj?.[key], item) 
          : item[field];
        
        return String(value).toLowerCase().includes(searchTerm.toLowerCase());
      });
    });
  };
  
  return {
    searchTerm,
    handleSearch,
    searchItems
  };
};
