/* eslint-disable operator-linebreak */
/* eslint-disable implicit-arrow-linebreak */
/* eslint-disable react/jsx-wrap-multilines */
/* eslint-disable no-unused-vars */
/* eslint-disable react/prop-types */
/* eslint-disable max-len */
import React, { useState, useEffect } from 'react';
import { nanoid } from 'nanoid';
import './reviews.css';
import { Link } from 'react-router-dom';
import Title from '../../ui/Title';

/*
import img5 from './img/content_merch_5.png';
import img6 from './img/content_merch_6.png';
import img7 from './img/content_merch_7.png';
import img8 from './img/content_merch_8.png'; */

export default function Reviews(/* { reviews } */) {
  // Заглушка для теста отзывов. Пришлось пока оставить так как с бэка не приходит, то что нужно.
  const reviews = [];
  const reviewsCount = 10; // Количество отзывов.
  for (let i = 1; i <= reviewsCount; i += 1) {
    reviews.push({
      item: { name: `${i}`, image: [{ image: 'https://dev.netomerch.tk/media/item/cup_uSeRI4R.jpeg' }] },
    });
  }
  console.log('reviews', reviews);
  // --------------------------------------------------------------------------------------------

  // Можно управлять количеством отображаемых отзывов и количеством листания.

  const [pos, setPos] = useState(0); // Начальная позиция в массиве отзывов, с которой отображаются видимые отзывы.
  const [vCount, setVCount] = useState(4); // Количество отображаемых отзывов (1 - 4).
  const [lCount, setLCount] = useState(4); // На сколько отзывов листается (1 - 4).
  const [vReviews, setVReviews] = useState([]); // Видимые отзывы.
  const [points, setPoints] = useState([]); // Массив для отрисовки точек слайдера.
  const [isSliderControl, setIsSliderControl] = useState(false); // Если все отзывы вмещаются на экран, тогда управление листанием скрыто.
  const [activePoint, setActivePoint] = useState(0); // Активная точка в слайдере. Указывает на позицию в массиве points.

  // Вычисляем массив видимых отзывов, при листании (или изменении количества видимых отзывов - пока не используется).
  useEffect(() => {
    const arr = [];
    const endPos = pos + vCount < reviews.length ? pos + vCount : reviews.length;
    for (let i = pos; i < endPos; i += 1) {
      arr.push(reviews[i]);
    }
    setVReviews(arr);
  }, [pos, vCount]);

  // Вычисляем массив для отрисовки точек.
  useEffect(() => {
    let pCount = Math.ceil((reviews.length - (vCount - lCount)) / lCount);
    if (pCount < 0) pCount = 1;
    const arr = [];
    for (let i = 0; i < pCount; i += 1) {
      arr.push('');
    }
    setPoints(arr);
  }, [vCount]);

  // Устанавливаем нужно ли показывать управление листанием слайдера.
  useEffect(() => {
    let isVisible = null;
    if (reviews.length <= vCount) isVisible = false;
    else isVisible = true;

    if (isSliderControl !== isVisible) setIsSliderControl(isVisible);
  }, [vCount]);

  // Вычисляем позицию активной точки для массива points.
  useEffect(() => {
    setActivePoint(Math.ceil(pos / lCount));
  }, [pos]);

  const handleOnRightClick = () => {
    let nextPos = pos + lCount;
    if ((nextPos > reviews.length) || (nextPos > reviews.length - vCount)) nextPos = reviews.length - vCount;
    if (nextPos < 0) nextPos = 0;
    if (pos !== nextPos) setPos(nextPos);
  };

  const handleOnLeftClick = () => {
    let nextPos = pos - lCount;
    if (nextPos < 0) nextPos = 0;
    if (pos !== nextPos) setPos(nextPos);
  };

  return (
    <div className="reviews">
      <div className="container">
        <Title cn="reviews__title" text="Блок с отзывами на товары" />
        <div className="reviews__text">
          Часто используемый в печати и вэб-дизайне. Lorem Ipsum является стандартной рыбой для текстов на латинице с начала XVI века. В то время некий безымянный для текстов на латинице с начала XVI века. В то время некий безымянный печатник создал большую коллекцию размеров и форм шрифтов, используя Lorem Ipsum.
        </div>

        {reviews.length !== 0 &&
        <div className="reviews__slider slider slider-rewiews">
          <div className="slider-rewiews__container">
            {vReviews.map((vReview) =>
              <div className="slider-rewiew" key={nanoid()}>
                <div className="slider-rewiew__img ibg">
                  <img src={vReview.item.image[0].image} alt={vReview.item.name} />
                </div>
                <a className="slider-rewiew__link" href="/#">{vReview.item.name}</a>
              </div>)}
          </div>

          {isSliderControl &&
          <div className="slider__control slider__control_gray slider-rewiews__control">
            <button className="slider__arrow" type="button" onClick={handleOnLeftClick}>
              <span className="visually-hidden">Назад</span>
            </button>

            <ul className="slider__points">
              {points.map((point, index) =>
                <li className={`slider__point${index === activePoint ? ' slider__point_active' : ''} `} key={nanoid()}>
                  <span className="visually-hidden">Точка слайдера</span>
                </li>)}
            </ul>

            <button className="slider__arrow slider__arrow_right" type="button" onClick={handleOnRightClick}>
              <span className="visually-hidden">Вперед</span>
            </button>
          </div>}
        </div>}

        <Link className="reviews__btn btn" to="/catalog">Мне все нравится, хочу такое же!</Link>
      </div>
    </div>
  );
}
