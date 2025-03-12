import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const Layout = ({ children }) => {
    const { logout, userData } = useAuth();
    const navigate = useNavigate();

    const handleLogout = () => {
        logout();
        navigate('/login');
    };

    const displayName = userData && userData.username ? userData.username : 'Admin';

    return (
        <div className="page">
          {/* Header */}
          <header className="navbar navbar-expand-md navbar-light d-print-none">
            <div className="container-xl">
              <h1 className="navbar-brand navbar-brand-autodark d-none-navbar-horizontal pe-0 pe-md-3">
                <Link to="/">
                  Vacancy Service
                </Link>
              </h1>
              
              <div className="navbar-nav flex-row order-md-last">
                <div className="nav-item dropdown">
                  <a href="#" className="nav-link d-flex lh-1 text-reset p-0" data-bs-toggle="dropdown">
                    <div className="d-none d-xl-block ps-2">
                      <span>{displayName }</span>
                    </div>
                  </a>
                  <div className="dropdown-menu dropdown-menu-end dropdown-menu-arrow">
                    <a href="#" className="dropdown-item" onClick={handleLogout}>Logout</a>
                  </div>
                </div>
              </div>
            </div>
          </header>
          
          {/* Navbar */}
          <div className="navbar-expand-md">
            <div className="collapse navbar-collapse" id="navbar-menu">
              <div className="navbar navbar-light">
                <div className="container-xl">
                  <ul className="navbar-nav">
                    <li className="nav-item">
                      <Link to="/" className="nav-link">
                        <span className="nav-link-icon d-md-none d-lg-inline-block">
                          <svg xmlns="http://www.w3.org/2000/svg" className="icon" width="24" height="24" viewBox="0 0 24 24" strokeWidth="2" stroke="currentColor" fill="none" strokeLinecap="round" strokeLinejoin="round">
                            <path stroke="none" d="M0 0h24v24H0z" fill="none" />
                            <polyline points="5 12 3 12 12 3 21 12 19 12" />
                            <path d="M5 12v7a2 2 0 0 0 2 2h10a2 2 0 0 0 2 -2v-7" />
                            <path d="M9 21v-6a2 2 0 0 1 2 -2h2a2 2 0 0 1 2 2v6" />
                          </svg>
                        </span>
                        <span className="nav-link-title">
                          Vacancies
                        </span>
                      </Link>
                    </li>
                    <li className="nav-item">
                      <Link to="/vacancies/create" className="nav-link">
                        <span className="nav-link-icon d-md-none d-lg-inline-block">
                          <svg xmlns="http://www.w3.org/2000/svg" className="icon" width="24" height="24" viewBox="0 0 24 24" strokeWidth="2" stroke="currentColor" fill="none" strokeLinecap="round" strokeLinejoin="round">
                            <path stroke="none" d="M0 0h24v24H0z" fill="none" />
                            <line x1="12" y1="5" x2="12" y2="19" />
                            <line x1="5" y1="12" x2="19" y2="12" />
                          </svg>
                        </span>
                        <span className="nav-link-title">
                          Create Vacancy
                        </span>
                      </Link>
                    </li>
                  </ul>
                  <div className="my-2 my-md-0 flex-grow-1 flex-md-grow-0 order-first order-md-last">
                    <form action="/" method="get">
                      <div className="input-icon">
                        <span className="input-icon-addon">
                          <svg xmlns="http://www.w3.org/2000/svg" className="icon" width="24" height="24" viewBox="0 0 24 24" strokeWidth="2" stroke="currentColor" fill="none" strokeLinecap="round" strokeLinejoin="round">
                            <path stroke="none" d="M0 0h24v24H0z" fill="none" />
                            <circle cx="10" cy="10" r="7" />
                            <line x1="21" y1="21" x2="15" y2="15" />
                          </svg>
                        </span>
                        <input type="text" className="form-control" placeholder="Search…" />
                      </div>
                    </form>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          {/* Page content */}
          <div className="page-wrapper">
            <div className="container-xl">
              <div className="page-header d-print-none">
                <div className="row align-items-center">
                  <div className="col">
                    <div className="page-pretitle">
                      Vacancy Service
                    </div>
                    <h2 className="page-title">
                      Manage Vacancies
                    </h2>
                  </div>
                </div>
              </div>
            </div>
            <div className="page-body">
              <div className="container-xl">
                {children}
              </div>
            </div>
            
            {/* Footer */}
            <footer className="footer footer-transparent d-print-none">
              <div className="container-xl">
                <div className="row text-center align-items-center flex-row-reverse">
                  <div className="col-lg-auto ms-lg-auto">
                    <ul className="list-inline list-inline-dots mb-0">
                      <li className="list-inline-item">
                        <a href="#" className="link-secondary">
                          Documentation
                        </a>
                      </li>
                      <li className="list-inline-item">
                        <a href="#" className="link-secondary">
                          Help
                        </a>
                      </li>
                    </ul>
                  </div>
                  <div className="col-12 col-lg-auto mt-3 mt-lg-0">
                    <ul className="list-inline list-inline-dots mb-0">
                      <li className="list-inline-item">
                        Copyright © 2025
                      </li>
                      <li className="list-inline-item">
                        <a href="#" className="link-secondary">
                          Vacancy Service
                        </a>
                      </li>
                    </ul>
                  </div>
                </div>
              </div>
            </footer>
          </div>
        </div>
    );
};

export default Layout;