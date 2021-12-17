/* eslint-disable jsx-a11y/label-has-associated-control */
/* eslint-disable react/prop-types */
/* eslint-disable no-unused-vars */
import React from 'react';
import styles from './catalogFilter.module.css';
import arrow from '../../../assets/img/filter_arrow.png';
import arrowDown from '../../../assets/img/filter_arrow_down.png';

const CatalogFilter = ({ categories, specialization }) => {
  console.log(categories, specialization);
  return (
    <section className={styles.filter}>

      <div className={styles.topPanel}>
        <ul className={styles.specialization}>
          <li className={styles.pressSpec}>Я маркетолог</li>
          <li>Я программист</li>
        </ul>
        <div className={styles.filterName}>
          <div className={styles.checkbox}>
            <input type="checkbox" className={styles.customCheckbox} id="popular" />
            <label htmlFor="popular">Сначала популярные</label>
          </div>
          <div className={styles.params}>
            Цена
            <img src={arrow} alt="arrow" />
          </div>
          <div className={styles.params}>
            Размер
            <img src={arrowDown} alt="arrow" />
          </div>
        </div>
      </div>

      <div className={styles.bottomPanel}>
        <ul className={styles.categories}>
          <li className={styles.pressCategory}>Худи</li>
          <li>Футболки</li>
          <li className={styles.dump} />
        </ul>
        <div className={styles.filterField}>
          <div className={styles.dopPanel}>
            <ul className={styles.price}>
              <li>
                По возрастанию 🠕
              </li>
              <li>
                По убыванию 🠗
              </li>
            </ul>
            <ul className={styles.size}>
              <li className={styles.press}>S</li>
              <li>M</li>
              <li>L</li>
            </ul>
          </div>
          <div className={styles.filterPrice}>
            По цене
            <label htmlFor="from">от</label>
            <input type="number" id="from" />
            <label htmlFor="to">до</label>
            <input type="number" id="to" />
          </div>
        </div>
      </div>
    </section>
  );
};

export default CatalogFilter;
