import React from 'react';
import styles from './product.module.css';
import ProductReviews from './ProductReviews/ProductReviews';

import mockData from './mockDataProductReviews.json';

const Product = () => {
  const { reviews } = mockData;

  return (
    <div className={styles.product}>
      <ProductReviews reviews={reviews} />
    </div>
  );
};

export default Product;
