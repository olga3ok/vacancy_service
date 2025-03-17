import React from 'react';
import Icon from './Icon';

const SearchBar = () => (
  <div className="my-2 my-md-0 flex-grow-1 flex-md-grow-0 order-first order-md-last">
    <form action="/" method="get">
      <div className="input-icon">
        <span className="input-icon-addon">
          <Icon name="search" />
        </span>
        <input type="text" className="form-control" placeholder="Search…" />
      </div>
    </form>
  </div>
);

export default SearchBar;