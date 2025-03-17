import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import Header from './Header';
import MainNav from './MainNav';
import PageHeader from './PageHeader';
import Footer from './Footer';

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
        <Header displayName={displayName} onLogout={handleLogout} />
        <MainNav />
        
        <div className="page-wrapper">
          <div className="container-xl">
            <PageHeader pretitle="Vacancy Service" title="Manage Vacancies" />
          </div>
          <div className="page-body">
            <div className="container-xl">
              {children}
            </div>
          </div>
          
          <Footer />
        </div>
      </div>
    );
};

export default Layout;