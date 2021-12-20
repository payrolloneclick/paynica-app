import React from 'react';
import { useTranslation } from 'react-i18next';
import { Button } from 'antd';

import logo from 'styles/img/logo.svg';

import styles from './index.module.scss';

const App = () => {
  const { t } = useTranslation();
  return (
    <div className={styles.app}>
      <header className={styles.appHeader}>
        <img src={logo} className={styles.appLogo} alt="logo" />
        <p>{t('Welcome to React')}</p>
        <Button type="primary">Primary Button</Button>
        <a
          className={styles.appLink}
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
};

export default App;
