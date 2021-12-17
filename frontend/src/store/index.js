import { createStore, applyMiddleware, combineReducers } from 'redux';
import thunk from 'redux-thunk';
import cartReducer from '../reducers/cartReducer';
import fetchCatalogReducer from '../reducers/fetchCatalogReducer';
import fetchMainPageReducer from '../reducers/fetchMainPageReducer';

const reducer = combineReducers({
  productInCart: cartReducer,
  fetchMainPage: fetchMainPageReducer,
  fetchCatalog: fetchCatalogReducer,
});

const store = createStore(
  reducer,
  applyMiddleware(thunk),
);

export default store;
