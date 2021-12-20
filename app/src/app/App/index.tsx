import React from 'react';
import { useTranslation } from 'react-i18next';
import { ConfigProvider, Button, Row, Col } from 'antd';

import styles from './index.module.scss';
import { useNavigate } from 'react-router-dom';

const App = () => {
  const { t } = useTranslation();
  const navigate = useNavigate();
  return (
    <ConfigProvider>
      <Row justify="center">
        <Col>
          <p className={styles.p}>{t('Welcome to App')}</p>
          <Button onClick={() => navigate('/admin')} type="primary">
            To Admin
          </Button>
        </Col>
      </Row>
    </ConfigProvider>
  );
};

export default App;
