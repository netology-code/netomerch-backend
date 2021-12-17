import React from 'react';
// import { Link } from 'react-router-dom';
import styles from './catalogBanner.module.css';

const CatalogBanner = () => (
  <div className={styles.banner}>
    <div className={styles.bannerTextContainer}>
      <p className={styles.bannerText}>Скидка 30% на стартовые наборы</p>
    </div>
    <div className={styles.bannerImage} />
  </div>
);

export default CatalogBanner;
