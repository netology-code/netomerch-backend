import React from 'react';
import styles from './cardOne.module.css';

const CardOne = () => (
  <div className={styles.card}>
    <h2>Моя первая карточка</h2>
    <div>
      Имя: Ольга
    </div>
    <div>
      Фронтенд-разработчик
    </div>
  </div>
);

export default CardOne;
