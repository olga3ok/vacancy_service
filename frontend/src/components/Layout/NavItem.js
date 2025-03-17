import React from 'react';
import { Link } from 'react-router-dom';
import Icon from './Icon';

const NavItem = ({ to, icon, title }) => (
  <li className="nav-item">
    <Link to={to} className="nav-link">
      <span className="nav-link-icon d-md-none d-lg-inline-block">
        <Icon name={icon} />
      </span>
      <span className="nav-link-title">{title}</span>
    </Link>
  </li>
);

export default NavItem;