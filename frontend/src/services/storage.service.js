const storageService = {
  get: (key) => (localStorage.getItem(key)
    ? JSON.parse(localStorage.getItem(key))
    : []),
  set: (key, data) => {
    localStorage.setItem(key, JSON.stringify(data));
  },
  add: (key, data) => {
    const cart = storageService.get(key);

    if (cart.length === 0) {
      storageService.set(key, data);
    } else {
      cart.push(data);
      storageService.set(key, cart);
    }
  },
  delete: (key, id) => {
    let cart = storageService.get(key);

    cart = cart.filter((prod) => prod.id !== id);
    storageService.set(key, cart);
  },
  clear: () => {
    localStorage.clear();
  },
};

export default storageService;
