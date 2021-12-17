import { useEffect } from 'react';
import { useLocation } from 'react-router-dom';

// нужен, чтобы при переходе по роутам возвращалось вверх страницы
const ScrollToTop = () => {
  const { pathname } = useLocation();

  useEffect(() => {
    window.scrollTo(0, 0);
  }, [pathname]);

  return null;
};

export default ScrollToTop;
