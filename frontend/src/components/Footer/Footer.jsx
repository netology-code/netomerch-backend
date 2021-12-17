import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import styles from './footer.module.css';
import logo from '../../assets/svg/logo_netology_full_white.svg';

const Footer = () => {
  const location = useLocation();

  if (location.pathname === '/notfaund') {
    return null;
  }

  return (
    <footer className={styles.footer}>
      <div className="max-container">
        <div className={styles.footerBody}>
          <div className={styles.footerColumn1}>
            <Link to="/" className={styles.footerLogo}>
              <img src={logo} alt="Logo Netologia" />
            </Link>
          </div>

          <div className={styles.footerColumn2}>
            <div className={styles.footerMenu}>
              <div className={`${styles.footerMenuColumn} ${styles.footerInfo}`}>
                <div className={styles.footerMenuLabel}>Информация</div>
                <ul className={`${styles.footerLinks} ${styles.footerLinksInfo}`}>
                  <li>
                    <Link to="/">Как заказать</Link>
                  </li>
                  <li>
                    <Link to="/">Доставка и оплата</Link>
                  </li>
                  <li>
                    <Link to="/">Приемка и возврат</Link>
                  </li>
                  <li>
                    <Link to="/">Пользовательское соглашение</Link>
                  </li>
                  <li>
                    <Link to="/">Конфиденциальность</Link>
                  </li>
                  <li>
                    <Link to="/">FAQ</Link>
                  </li>
                </ul>
              </div>
              <div className={`${styles.footerMenuColumn} ${styles.footerMerch}`}>
                <div className={styles.footerMenuLabel}>Netology Grow Merch</div>
                <ul className={`${styles.footerLinks} ${styles.footerLinksMerch}`}>
                  <li>
                    <Link to="/">О нас</Link>
                  </li>
                  <li>
                    <Link to="/">Каталог</Link>
                  </li>
                  <li>
                    <Link to="/">Отзывы</Link>
                  </li>
                </ul>
                <div className={styles.footerSocial}>
                  <div className={styles.footerFacebook} />
                  <div className={styles.footerTelegram} />
                  <div className={styles.footerYoutube} />
                  <div className={styles.footerInstagram} />
                  <div className={styles.footerVkontakte} />
                </div>
              </div>
              <div className={`${styles.footerMenuColumn} ${styles.footerProducts}`}>
                <div className={styles.footerMenuLabel}>Каталог по товарам</div>
                <ul className={`${styles.footerLinks} ${styles.footerLinksProducts}`}>
                  <li>
                    <Link to="/">Толстовки</Link>
                  </li>
                  <li>
                    <Link to="/">Худи</Link>
                  </li>
                  <li>
                    <Link to="/">Футболки</Link>
                  </li>
                  <li>
                    <Link to="/">Канцтовары</Link>
                  </li>
                  <li>
                    <Link to="/">Стикеры</Link>
                  </li>
                  <li>
                    <Link to="/">Стартовый набор</Link>
                  </li>
                </ul>
              </div>
              <div className={`${styles.footerMenuColumn} ${styles.footerCategories}`}>
                <div className={styles.footerMenuLabel}>Каталог по направлениям</div>
                <ul className={`${styles.footerLinks} ${styles.footerLinksCategories}`}>
                  <li>
                    <Link to="/">Маркетинг</Link>
                  </li>
                  <li>
                    <Link to="/">Бизнес и управление</Link>
                  </li>
                  <li>
                    <Link to="/">Дизайн</Link>
                  </li>
                  <li>
                    <Link to="/">Программирование</Link>
                  </li>
                </ul>
              </div>
              <div className={`${styles.footerMenuColumn} ${styles.footerAdditional}`}>
                <div className={styles.footerInline}>
                  <div className={styles.footerMenuLabel}>Перейти в корзину</div>
                  <div className={styles.footerCart} />
                </div>
                <div className={styles.footerAdditional}>
                  <div className={styles.footerMenuLabel}>Центр поддержки</div>
                  <ul className={`${styles.footerLinks} ${styles.footerLinksAdditional}`}>
                    <li>
                      <Link to="/">8 800 123-45-67 для вас 24/7</Link>
                    </li>
                    <li>
                      <Link to="/">Отправить сообщение</Link>
                    </li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
