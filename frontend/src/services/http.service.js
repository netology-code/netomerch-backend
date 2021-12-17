import config from '../config.json';

const httpService = {
  get: (endPoint) => fetch(`${config.apiEndPoint}${endPoint}`),
};

export default httpService;
