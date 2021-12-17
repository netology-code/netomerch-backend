/* eslint-disable react/jsx-wrap-multilines */
/* eslint-disable implicit-arrow-linebreak */
/* eslint-disable react/no-array-index-key */
import React, { useEffect, useState } from 'react';
import './main-top.css';
import '../Slider/slider.css';

import img1 from './img/content_merch_1.jpg';
import img2 from './img/content_merch_2.jpg';
import img3 from './img/content_merch_3.jpg';
import img4 from './img/content_merch_4.jpg';
import img5 from './img/content_merch_5.jpg';
import img6 from './img/content_merch_6.jpg';
import img7 from './img/content_merch_7.jpg';

export default function MainTop() {
  const imgs = [img1, img2, img3, img4, img5, img6, img7];
  const [imgCurr, setImgCurr] = useState(0);

  const handleOnRightClick = () => {
    if (imgCurr === imgs.length - 1) setImgCurr(0);
    else setImgCurr(imgCurr + 1);
  };

  const handleOnLeftClick = () => {
    if (imgCurr === 0) setImgCurr(imgs.length - 1);
    else setImgCurr(imgCurr - 1);
  };

  useEffect(() => {
    const timeout = setTimeout(() => handleOnRightClick(), 5000);
    return () => clearTimeout(timeout);
  }, [imgCurr]);

  return (
    <div className="main-top">
      <div className="container">
        <div className="slider slider-main">
          <div className="slider-main__img ibg">
            <img src={imgs[imgCurr]} alt="slider" />
          </div>
          <div className="slider__control slider-main__control">
            <button className="slider__arrow" type="button" onClick={handleOnLeftClick}>
              <span className="visually-hidden">Назад</span>
            </button>

            <ul className="slider__points">
              {imgs.map((img, index) =>
                <li
                  key={index}
                  className={`slider__point${index === imgCurr ? ' slider__point_active' : ''}`}
                >
                  <span className="visually-hidden">Точка слайдера</span>
                </li>)}
            </ul>

            <button className="slider__arrow slider__arrow_right" type="button" onClick={handleOnRightClick}>
              <span className="visually-hidden">Вперед</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
