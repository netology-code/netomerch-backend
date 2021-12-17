import React from 'react';
import { Link } from 'react-router-dom';
import styles from './error404.module.css';

const error404 = () => (
  <div className={styles.error}>
    <div className={styles.main}>
      <div className={styles.number} />
      <div className={styles.image} />
      <p className={styles.text}>Страница не найдена</p>
      <div className={styles.button}>
        <Link to="/">На главную</Link>
      </div>
    </div>
  </div>
);

export default error404;
