import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import styles from './header.module.css';
import logo from '../../assets/svg/logo_netology_full.svg';

const Header = () => {
  const location = useLocation();

  if (location.pathname === '/notfaund') {
    return null;
  }

  return (
    <header className={styles.header}>
      <div className="max-container">
        <div className={styles.headerBody}>
          <Link to="/" className={styles.headerLogo}>
            <img src={logo} alt="Logo Netologia" />
          </Link>
          <nav className={styles.headerMenu}>
            <ul className={styles.headerMenuList}>
              <li>
                <Link to="/catalog">Каталог</Link>
              </li>
              <li>
                <Link to="/">О Нетологии</Link>
              </li>
              <li>
                <Link to="/support">Центр поддержки</Link>
              </li>
            </ul>
          </nav>
          <div className={styles.headerIcons}>
            {/* <div className={styles.headerSearch} /> */}
            <Link to="/">
              <div className={styles.headerHelp} />
            </Link>
            <Link to="/cart">
              <div className={styles.headerCart} />
            </Link>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
