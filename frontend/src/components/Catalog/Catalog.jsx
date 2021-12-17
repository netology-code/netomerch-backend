import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import CatalogBanner from './CatalogBanner/CatalogBanner';
import CatalogItems from './CatalogItems/CatalogItems';
import styles from './catalog.module.css';
import { fetchCatalog } from '../../actions/actionCreators';
import Loader from '../Loader/Loader';
import Error from '../Error/Error';
import CatalogFilter from './CatalogFilter/CatalogFilter';
import mockData from './mockDataCatalog.json';

const Catalog = () => {
  const {
    catalog, categories, specialization, error, loading,
  } = useSelector((state) => state.fetchCatalog);
  const dispatch = useDispatch();
  const { items } = mockData;

  useEffect(() => {
    dispatch(fetchCatalog());
  }, []);

  if (loading) {
    return <Loader />;
  }

  if (error) {
    return <Error message={error} />;
  }

  console.log(catalog, categories, specialization);

  return (
    <div className={styles.catalog}>
      <CatalogBanner />
      <CatalogFilter categories={categories} specialization={specialization} />
      <CatalogItems items={items} />
    </div>
  );
};

export default Catalog;
