import React from 'react';
import styles from './cardThree.module.css';

const CardThree = () => (
  <div className={styles.card}>
    <h2>Моя третья карточка</h2>
    <img src="https://netology-code.github.io/mq-homeworks/fluid-images/phone-book/img/mabel.jpeg" alt="avatar" />
    <div>
      Имя: Aнна
    </div>
    <div>
      Фронтенд-разработчик
    </div>
  </div>
);

export default CardThree;
