/* eslint-disable no-unused-vars */
/* eslint-disable max-len */
/* eslint-disable react/prop-types */
import React, { useState, useEffect } from 'react';
import { nanoid } from 'nanoid';
import styles from './productReviews.module.css';
import ProductReview from './ProductReview/ProductReview';

export default function ProductReviews(props) {
  const { reviews } = props;

  // Можно управлять количеством отображаемых отзывов и количеством листания.
  const [pos, setPos] = useState(0); // Начальная позиция в массиве отзывов, с которой отображаются видимые отзывы.
  const [vCount, setVCount] = useState(3); // Количество отображаемых отзывов (1 - 3).
  const [lCount, setLCount] = useState(1); // На сколько отзывов листается (1 - 3).
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
    <div className="container">
      {reviews.length !== 0 && (
        <div className="reviews__slider slider">
          <div className={styles.productReviews_reviews_block}>
            <div className={styles.productReviews_content}>
              {vReviews.map((review) => (
                <ProductReview
                  key={nanoid()}
                  id={review.id}
                  text={review.text}
                  author={review.author}
                  author_image={review.author_image}
                  date={review.date}
                />
              ))}
            </div>

            {isSliderControl && (
            <div className="slider__control slider__control_gray slider-rewiews__control">
              <button className="slider__arrow" type="button" onClick={handleOnLeftClick}>
                <span className="visually-hidden">Назад</span>
              </button>

              <ul className="slider__points">
                {points.map((point, index) => (
                  <li className={`slider__point${index === activePoint ? ' slider__point_active' : ''} `} key={nanoid()}>
                    <span className="visually-hidden">Точка слайдера</span>
                  </li>
                ))}
              </ul>
              <button className="slider__arrow slider__arrow_right" type="button" onClick={handleOnRightClick}>
                <span className="visually-hidden">Вперед</span>
              </button>
            </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
