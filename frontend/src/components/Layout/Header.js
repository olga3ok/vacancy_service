import React from 'react';
import { Link } from 'react-router-dom';

const Header = ({ displayName, onLogout }) => (
  <header className="navbar navbar-expand-md navbar-light d-print-none">
    <div className="container-xl">
      <h1 className="navbar-brand navbar-brand-autodark d-none-navbar-horizontal pe-0 pe-md-3">
        <Link to="/">Vacancy Service</Link>
      </h1>
      
      <div className="navbar-nav flex-row order-md-last">
        <div className="nav-item dropdown">
          <a href="#" className="nav-link d-flex lh-1 text-reset p-0" data-bs-toggle="dropdown">
            <div className="d-none d-xl-block ps-2">
              <span>{displayName}</span>
            </div>
          </a>
          <div className="dropdown-menu dropdown-menu-end dropdown-menu-arrow">
            <a href="#" className="dropdown-item" onClick={onLogout}>Logout</a>
          </div>
        </div>
      </div>
    </div>
  </header>
);

export default Header;