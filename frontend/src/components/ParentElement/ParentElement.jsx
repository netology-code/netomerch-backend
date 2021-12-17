/* eslint-disable react/prop-types */
import React from 'react';
import Footer from '../Footer/Footer';
import Header from '../Header/Header';

const ParentElement = ({ children }) => (
  <div className="wrapper">
    <Header />
    <main className="main">
      { children }
    </main>
    <Footer />
  </div>
);

export default ParentElement;
