import { useEffect, useMemo, useState } from "react";

import { analyticsApi, paymentApi, productApi, subscriptionApi } from "../api/services";
import { useToast } from "../context/ToastContext";

function AdminDashboard() {
  const { pushToast } = useToast();
  const [dashboard, setDashboard] = useState(null);
  const [demand, setDemand] = useState([]);
  const [growth, setGrowth] = useState([]);
  const [subscriptions, setSubscriptions] = useState([]);
  const [payments, setPayments] = useState([]);
  const [products, setProducts] = useState([]);
  const [categories, setCategories] = useState([]);
  const [newProduct, setNewProduct] = useState({
    category: "",
    name: "",
    description: "",
    image_url: "",
    price: "",
    stock_quantity: "",
    unit: "pack",
  });
  const [priceUpdate, setPriceUpdate] = useState({ productId: "", amount: "" });

  const loadData = async () => {
    const [
      dashboardResponse,
      demandResponse,
      growthResponse,
      subscriptionsResponse,
      paymentsResponse,
      productsResponse,
      categoriesResponse,
    ] = await Promise.all([
      analyticsApi.dashboard(),
      analyticsApi.demand(),
      analyticsApi.growth(),
      subscriptionApi.list(),
      paymentApi.list(),
      productApi.list(),
      productApi.categories(),
    ]);

    setDashboard(dashboardResponse.data);
    setDemand(demandResponse.data);
    setGrowth(growthResponse.data);
    setSubscriptions(subscriptionApi.normalizeList(subscriptionsResponse.data));
    setPayments(paymentApi.normalizeList(paymentsResponse.data));
    setProducts(productApi.normalizeList(productsResponse.data));
    setCategories(categoriesResponse.data?.results || categoriesResponse.data || []);
  };

  useEffect(() => {
    loadData().catch(() => pushToast("Unable to load admin dashboard.", "error"));
  }, [pushToast]);

  const chartMax = useMemo(() => Math.max(...growth.map((item) => item.total), 1), [growth]);

  const addProduct = async (event) => {
    event.preventDefault();
    try {
      await productApi.create({
        ...newProduct,
        price: Number(newProduct.price),
        stock_quantity: Number(newProduct.stock_quantity),
      });
      pushToast("Product added successfully.", "success");
      setNewProduct({
        category: "",
        name: "",
        description: "",
        image_url: "",
        price: "",
        stock_quantity: "",
        unit: "pack",
      });
      await loadData();
    } catch {
      pushToast("Product creation failed.", "error");
    }
  };

  const increasePrice = async (event) => {
    event.preventDefault();
    if (!priceUpdate.productId || !priceUpdate.amount) return;
    try {
      await productApi.increasePrice(priceUpdate.productId, Number(priceUpdate.amount));
      pushToast("Price updated.", "success");
      setPriceUpdate({ productId: "", amount: "" });
      await loadData();
    } catch {
      pushToast("Price update failed.", "error");
    }
  };

  return (
    <main className="mx-auto max-w-7xl space-y-6 px-4 py-8 md:px-6">
      <h1 className="font-serif text-3xl font-bold text-black">Admin Dashboard</h1>

      <section className="grid gap-4 md:grid-cols-3 lg:grid-cols-6">
        <Metric title="Customers" value={dashboard?.total_customers || 0} />
        <Metric title="Subscriptions" value={dashboard?.total_subscriptions || 0} />
        <Metric title="Active" value={dashboard?.active_subscriptions || 0} />
        <Metric title="Revenue (Month)" value={`Rs ${dashboard?.revenue_this_month || "0.00"}`} />
        <Metric title="Revenue (Total)" value={`Rs ${dashboard?.revenue_total || "0.00"}`} />
        <Metric title="Most Demanded" value={dashboard?.most_demanded_product || "-"} />
      </section>

      <section className="card-surface p-5">
        <h2 className="font-serif text-2xl text-black">Subscription Growth</h2>
        <div className="mt-4 grid grid-cols-2 gap-3 md:grid-cols-6">
          {growth.map((item) => (
            <div key={item.month} className="rounded-xl border border-[#EAEAEA] bg-white p-3 text-center">
              <div
                className="mx-auto mb-2 w-8 rounded-t bg-lightBlue"
                style={{ height: `${Math.max(12, (item.total / chartMax) * 90)}px` }}
              />
              <p className="text-xs text-[#333333]">{item.month}</p>
              <p className="text-sm font-semibold text-black">{item.total}</p>
            </div>
          ))}
        </div>
      </section>

      <section className="grid gap-4 lg:grid-cols-2">
        <div className="card-surface p-5">
          <h3 className="font-serif text-xl text-black">Add Product</h3>
          <form onSubmit={addProduct} className="mt-3 space-y-2">
            <select
              value={newProduct.category}
              onChange={(event) => setNewProduct((prev) => ({ ...prev, category: event.target.value }))}
              className="input-field"
              required
            >
              <option value="">Select category</option>
              {categories.map((item) => (
                <option key={item.id} value={item.id}>
                  {item.name}
                </option>
              ))}
            </select>
            <input
              value={newProduct.name}
              onChange={(event) => setNewProduct((prev) => ({ ...prev, name: event.target.value }))}
              placeholder="Product name"
              className="input-field"
              required
            />
            <input
              value={newProduct.image_url}
              onChange={(event) => setNewProduct((prev) => ({ ...prev, image_url: event.target.value }))}
              placeholder="Image URL"
              className="input-field"
            />
            <textarea
              value={newProduct.description}
              onChange={(event) => setNewProduct((prev) => ({ ...prev, description: event.target.value }))}
              placeholder="Description"
              className="input-field min-h-20"
            />
            <div className="grid grid-cols-3 gap-2">
              <input
                value={newProduct.price}
                onChange={(event) => setNewProduct((prev) => ({ ...prev, price: event.target.value }))}
                placeholder="Price"
                type="number"
                className="input-field"
                required
              />
              <input
                value={newProduct.stock_quantity}
                onChange={(event) => setNewProduct((prev) => ({ ...prev, stock_quantity: event.target.value }))}
                placeholder="Stock"
                type="number"
                className="input-field"
                required
              />
              <select
                value={newProduct.unit}
                onChange={(event) => setNewProduct((prev) => ({ ...prev, unit: event.target.value }))}
                className="input-field"
              >
                <option value="litre">Litre</option>
                <option value="kg">Kg</option>
                <option value="pack">Pack</option>
              </select>
            </div>
            <button className="btn-primary rounded-xl px-4 py-2 text-sm">Add Product</button>
          </form>
        </div>

        <div className="card-surface p-5">
          <h3 className="font-serif text-xl text-black">Increase Product Price</h3>
          <form onSubmit={increasePrice} className="mt-3 space-y-2">
            <select
              value={priceUpdate.productId}
              onChange={(event) => setPriceUpdate((prev) => ({ ...prev, productId: event.target.value }))}
              className="input-field"
              required
            >
              <option value="">Select product</option>
              {products.map((product) => (
                <option key={product.id} value={product.id}>
                  {product.name}
                </option>
              ))}
            </select>
            <input
              value={priceUpdate.amount}
              onChange={(event) => setPriceUpdate((prev) => ({ ...prev, amount: event.target.value }))}
              type="number"
              step="0.01"
              placeholder="Increase amount"
              className="input-field"
              required
            />
            <button className="btn-secondary rounded-xl px-4 py-2 text-sm">Increase</button>
          </form>
        </div>
      </section>

      <section className="grid gap-4 lg:grid-cols-2">
        <Panel title="Subscription History">
          {subscriptions.map((sub) => (
            <p key={sub.id} className="rounded-xl border border-[#EAEAEA] p-3 text-sm text-[#333333]">
              {sub.user_email} subscribed {sub.product_name} ({sub.frequency}) from {sub.start_date} to {sub.estimated_end_date}
            </p>
          ))}
        </Panel>
        <Panel title="Payment Status">
          {payments.map((payment) => (
            <p key={payment.id} className="rounded-xl border border-[#EAEAEA] p-3 text-sm text-[#333333]">
              {payment.user_email} - {payment.transaction_id} - Rs {payment.amount} ({payment.status})
            </p>
          ))}
        </Panel>
      </section>

      <section className="card-surface p-5">
        <h3 className="font-serif text-xl text-black">Product Demand Statistics</h3>
        <div className="mt-3 grid gap-2 sm:grid-cols-2">
          {demand.map((item) => (
            <p key={item.product_id} className="rounded-xl border border-[#EAEAEA] p-3 text-sm text-[#333333]">
              {item.product_name}: {item.demand_count}
            </p>
          ))}
        </div>
      </section>
    </main>
  );
}

function Metric({ title, value }) {
  return (
    <div className="rounded-xl border border-[#EAEAEA] border-l-[5px] border-l-primary bg-white p-4 shadow-sm">
      <p className="text-xs uppercase tracking-wide text-[#333333]">{title}</p>
      <p className="mt-1 text-lg font-bold text-black">{value}</p>
    </div>
  );
}

function Panel({ title, children }) {
  return (
    <div className="card-surface p-5">
      <h3 className="font-serif text-xl text-black">{title}</h3>
      <div className="mt-3 space-y-2">{children}</div>
    </div>
  );
}

export default AdminDashboard;
