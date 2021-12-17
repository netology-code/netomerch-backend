import { UPDATE_CART } from '../actions/actionTypes';
import storageService from '../services/storage.service';

const initialState = {
  products: storageService.get('cart'),
};

function cartReducer(state = initialState, action) {
  switch (action.type) {
    case UPDATE_CART:
      return { ...state, products: storageService.get('cart') };
    default:
      return state;
  }
}

export default cartReducer;
