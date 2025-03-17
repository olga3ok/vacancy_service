import React from 'react';

const PageHeader = ({ pretitle, title }) => (
  <div className="page-header d-print-none">
    <div className="row align-items-center">
      <div className="col">
        {pretitle && <div className="page-pretitle">{pretitle}</div>}
        {title && <h2 className="page-title">{title}</h2>}
      </div>
    </div>
  </div>
);

export default PageHeader;