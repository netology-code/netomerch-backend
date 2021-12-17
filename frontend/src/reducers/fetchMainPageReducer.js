/* eslint-disable no-case-declarations */
import { FETCH_MAINPAGE_FAILURE, FETCH_MAINPAGE_START, FETCH_MAINPAGE_SUCCESS } from '../actions/actionTypes';

const initialState = {
  reviews: [],
  popular: [],
  loading: false,
  error: null,
};

function fetchMainPageReducer(state = initialState, action) {
  switch (action.type) {
    case FETCH_MAINPAGE_START:
      return { ...state, loading: true };
    case FETCH_MAINPAGE_FAILURE:
      const { error } = action.payload;
      return { ...state, loading: false, error };
    case FETCH_MAINPAGE_SUCCESS:
      const { data } = action.payload;
      return {
        reviews: data.reviews, popular: data.popular, loading: false, error: null,
      };
    default:
      return state;
  }
}

export default fetchMainPageReducer;
