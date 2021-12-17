import React from 'react';
// import { Link } from 'react-router-dom';
import styles from './madeBy.module.css';
import Title from '../../ui/Title';

const MadeBy = () => (
  <div className={styles.madeBy}>
    <div className="container">
      <div className={styles.madeByBody}>
        <div className={styles.madeByStar} />
        <Title cn={styles.madeByHeading} text="информационный блок о создателях сайта" sqColor="green" />
        <div className={styles.madeByPhotos}>
          <div className={styles.madeByPhoto} />
          <div className={styles.madeByPhoto} />
          <div className={styles.madeByPhoto} />
          <div className={styles.madeByPhoto} />
          <div className={styles.madeByPhoto} />
          <div className={styles.madeByPhoto} />
          <div className={styles.madeByPhoto} />
          <div className={styles.madeByPhoto} />
          <div className={styles.madeByPhoto} />
          <div className={styles.madeByPhoto} />
          <div className={styles.madeByPhoto} />
          <div className={styles.madeByPhoto} />
          <div className={styles.madeByPhoto} />
          <div className={styles.madeByPhoto} />
          <div className={styles.madeByPhoto} />
          <div className={styles.madeByPhoto} />
        </div>
        <div className={styles.madeByDescription}>
          <h3 className={styles.madeByMinorLabel}>О создателях сайта</h3>
          <p className={styles.madeByText}>О создателях сайта</p>
          <a href="/" className={styles.madeByLink}>О создателях сайта</a>
        </div>
      </div>
    </div>
  </div>
);

export default MadeBy;
