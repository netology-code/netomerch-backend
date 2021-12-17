import React from 'react';
import { Provider } from 'react-redux';
import configureStore from 'redux-mock-store';
import { render, screen } from '@testing-library/react';
import App from './App';

test('renders text App', () => {
  store = mockStore(initialState);
  const { getByText } = render(
      <Provider store={store}>
          <App />
      </Provider>
  );
  expect(screen.getByText('Hello World!!!')).toBeInTheDocument();
});
