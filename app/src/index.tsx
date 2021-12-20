import React from 'react';
import ReactDOM from 'react-dom';
import { ConfigProvider } from 'antd';
import enUS from 'antd/es/locale/en_US';
import { HelmetProvider } from 'react-helmet-async';
import { QueryClient, QueryClientProvider } from 'react-query';

import App from 'containers/App';

import './i18n';
import reportWebVitals from './reportWebVitals';

import 'styles/index.scss';

const queryClient = new QueryClient();

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

ReactDOM.render(
  <React.StrictMode>
    <ConfigProvider locale={enUS}>
      <HelmetProvider>
        <QueryClientProvider client={queryClient}>
          <App />
        </QueryClientProvider>
      </HelmetProvider>
    </ConfigProvider>
  </React.StrictMode>,
  document.getElementById('root'),
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
