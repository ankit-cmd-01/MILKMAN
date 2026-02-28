import client from "./client";

const normalizeList = (payload) => {
  if (Array.isArray(payload)) return payload;
  if (Array.isArray(payload?.results)) return payload.results;
  return [];
};

export const authApi = {
  login: (data) => client.post("/auth/login/", data),
  register: (data) => client.post("/auth/register/", data),
  profile: () => client.get("/auth/profile/"),
  updateProfile: (data) => client.patch("/auth/profile/", data),
};

export const productApi = {
  list: (params = {}) => client.get("/products/items/", { params }),
  categories: () => client.get("/products/categories/"),
  create: (data) => client.post("/products/items/", data),
  increasePrice: (id, amount) => client.patch(`/products/items/${id}/increase_price/`, { amount }),
  normalizeList,
};

export const subscriptionApi = {
  list: (params = {}) => client.get("/subscriptions/", { params }),
  create: (data) => client.post("/subscriptions/", data),
  bulkCreate: (items) => client.post("/subscriptions/bulk_subscribe/", { items }),
  pause: (id) => client.patch(`/subscriptions/${id}/pause/`),
  resume: (id) => client.patch(`/subscriptions/${id}/resume/`),
  cancel: (id) => client.patch(`/subscriptions/${id}/cancel/`),
  history: (id) => client.get(`/subscriptions/${id}/history/`),
  adminOverview: () => client.get("/subscriptions/admin_overview/"),
  normalizeList,
};

export const cartApi = {
  detail: () => client.get("/cart/"),
  add: (product_id, quantity = 1) => client.post("/cart/items/", { product_id, quantity }),
  update: (itemId, quantity) => client.patch(`/cart/items/${itemId}/`, { quantity }),
  remove: (itemId) => client.delete(`/cart/items/${itemId}/`),
  checkout: (payment_method) => client.post("/cart/checkout/", { payment_method }),
  oneTimeOrders: () => client.get("/cart/orders/"),
};

export const paymentApi = {
  list: () => client.get("/payments/"),
  create: (data) => client.post("/payments/", data),
  updateStatus: (id, status) => client.patch(`/payments/${id}/update_status/`, { status }),
  normalizeList,
};

export const analyticsApi = {
  dashboard: () => client.get("/analytics/dashboard/"),
  demand: () => client.get("/analytics/product-demand/"),
  growth: () => client.get("/analytics/subscription-growth/"),
};
