import React from 'react';
import NavItem from './NavItem';
import SearchBar from './SearchBar';

const MainNav = () => (
  <div className="navbar-expand-md">
    <div className="collapse navbar-collapse" id="navbar-menu">
      <div className="navbar navbar-light">
        <div className="container-xl">
          <ul className="navbar-nav">
            <NavItem to="/" icon="home" title="Vacancies" />
            <NavItem to="/vacancies/create" icon="add" title="Create Vacancy" />
          </ul>
          <SearchBar />
        </div>
      </div>
    </div>
  </div>
);

export default MainNav;