/* eslint-disable jsx-a11y/no-static-element-interactions */
/* eslint-disable jsx-a11y/click-events-have-key-events */
/* eslint-disable react/prop-types */
import React from 'react';
import style from './accordion.module.css';
import accordOpen from '../../../assets/img/accordion_open.png';
import accordClose from '../../../assets/img/accordion_close.png';

const Accordion = ({
  id, title, content, isOpen, onClick,
}) => (
  <div className={`${style.item} ${isOpen ? style.open : ''}`}>
    <div className={style.title} onClick={() => onClick(id)}>
      <div className={style.icon}>
        <img src={isOpen ? accordOpen : accordClose} alt="icon" />
      </div>
      <p>{title}</p>
      <div className={style.cross}> </div>
    </div>
    <div className={style.content}>
      <div>
        <div className={style.line}> </div>
        <p>{content}</p>
      </div>
    </div>
  </div>
);

export default Accordion;
