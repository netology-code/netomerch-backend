/* eslint-disable camelcase */
/* eslint-disable no-unused-vars */
/* eslint-disable react/prop-types */
import React from 'react';
import styles from './productReview.module.css';

const ProductReview = (props) => {
  const {
    id, text, author, author_image, date,
  } = props;

  return (
    <div className={styles.productReview_review}>
      <div className={styles.productReview_item}>
        <div className={styles.productReview_person}>
          <img className={styles.productReview_img} src={author_image} alt="avatar" />
          <h4 className={styles.productReview_title}>{author}</h4>
        </div>

        <p className={styles.productReview_content}>{text}</p>
        <time className={styles.productReview_date}>{date}</time>
      </div>
    </div>
  );
};

export default ProductReview;
