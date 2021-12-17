import React from 'react';
import { render, screen } from '@testing-library/react';
import App from './App';
import { Provider } from 'react-redux';

test('renders text App', () => {
  render(<App />);
  expect(screen.getByText('Hello World!!!')).toBeInTheDocument();
});
