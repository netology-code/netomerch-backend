/* eslint-disable object-curly-newline */
/* eslint-disable react/prop-types */

/**
 * cn (className) - можно указать дополнительные классы для блока title,
 * которые, например, определют отступы. Принимает строку с перечислением классов через пробел
 * или css модуль.
 *
 * text - текст заголовка
 *
 * sqColor (square color) - цвет квадрата.
 * По умолчанию цвет синий (Netology_blue1).
 *
 * sqSize - размер квадрата
 * По умолчанию размер 30px.
 */

import React from 'react';
import './title.css';

export default function Title({ cn, text, sqColor, sqSize }) {
  const titleClasses = ['title'];
  if (cn) titleClasses.push(...cn.split(' '));

  if (sqColor) {
    const sqColors = {
      pink: 'title_pink',
      green: 'title_green',
      purple: 'title_purple',
    };
    titleClasses.push(sqColors[sqColor]);
  }

  if (sqSize) {
    const sqSizes = {
      25: 'title_size-25',
    };
    titleClasses.push(sqSizes[sqSize]);
  }

  return (
    <h2 className={titleClasses.join(' ')}>{text}</h2>
  );
}
