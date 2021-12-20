import React from 'react';
import { Routes, Route } from 'react-router-dom';
import { ConfigProvider } from 'antd';

import Admin from 'admin/Admin';
import App from 'app/App';

ConfigProvider.config({
  theme: {
    primaryColor: '#84aea3',
    infoColor: '#7a92ce',
    successColor: '#ff7851',
    processingColor: '#8d7091',
    errorColor: '#ff4d4f',
    warningColor: '#cea709',
  },
});

const Bootstrap = () => {
  return (
    <Routes>
      <Route path="admin" element={<Admin />} />
      <Route path="*" element={<App />} />
    </Routes>
  );
};

export default Bootstrap;
