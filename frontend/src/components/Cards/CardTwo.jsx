import React from 'react';
import styles from './cardTwo.module.css';

const CardTwo = () => (
  <div className={styles.card}>
    <h2>Моя вторая карточка</h2>
    <div>
      Имя: Кирилл
    </div>
    <div>
      Разработчик зануда
    </div>
  </div>
);

export default CardTwo;
