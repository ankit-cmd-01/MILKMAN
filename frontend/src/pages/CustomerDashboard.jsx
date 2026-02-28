import { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";

import { authApi, cartApi, paymentApi, subscriptionApi } from "../api/services";
import { useAuth } from "../context/AuthContext";
import { useToast } from "../context/ToastContext";

function CustomerDashboard() {
  const { user, updateProfile } = useAuth();
  const { pushToast } = useToast();
  const [subscriptions, setSubscriptions] = useState([]);
  const [payments, setPayments] = useState([]);
  const [cart, setCart] = useState(null);
  const [orders, setOrders] = useState([]);
  const [address, setAddress] = useState(user?.address || "");

  const loadDashboard = async () => {
    const [subscriptionResponse, paymentResponse, cartResponse, orderResponse] = await Promise.all([
      subscriptionApi.list(),
      paymentApi.list(),
      cartApi.detail(),
      cartApi.oneTimeOrders(),
    ]);

    setSubscriptions(subscriptionApi.normalizeList(subscriptionResponse.data));
    setPayments(paymentApi.normalizeList(paymentResponse.data));
    setCart(cartResponse.data);
    const rawOrders = orderResponse.data?.results || orderResponse.data;
    setOrders(Array.isArray(rawOrders) ? rawOrders : []);
  };

  useEffect(() => {
    loadDashboard().catch(() => pushToast("Unable to load dashboard data.", "error"));
  }, [pushToast]);

  const activeSubscriptions = useMemo(
    () => subscriptions.filter((item) => item.status === "ACTIVE"),
    [subscriptions]
  );
  const dailySubscriptions = useMemo(
    () => activeSubscriptions.filter((item) => item.frequency === "DAILY"),
    [activeSubscriptions]
  );

  const updateSubStatus = async (id, action) => {
    const actionApi = {
      pause: subscriptionApi.pause,
      resume: subscriptionApi.resume,
      cancel: subscriptionApi.cancel,
    };
    try {
      await actionApi[action](id);
      await loadDashboard();
      pushToast(`Subscription ${action}d.`, "success");
    } catch {
      pushToast("Unable to update subscription.", "error");
    }
  };

  const saveAddress = async () => {
    try {
      await updateProfile({ address });
      await authApi.profile();
      pushToast("Address updated.", "success");
    } catch {
      pushToast("Address update failed.", "error");
    }
  };

  return (
    <main className="mx-auto max-w-7xl space-y-6 px-4 py-8 md:px-6">
      <h1 className="font-serif text-3xl font-bold text-black">Customer Dashboard</h1>

      <section className="grid gap-4 md:grid-cols-4">
        <Metric title="Active Subscriptions" value={activeSubscriptions.length} />
        <Metric title="Daily Products" value={dailySubscriptions.length} />
        <Metric title="Cart Items" value={cart?.items?.length || 0} />
        <Metric title="Payments" value={payments.length} />
      </section>

      <section className="card-surface p-5">
        <div className="flex items-center justify-between">
          <h2 className="font-serif text-2xl text-black">My Active Subscriptions</h2>
          <Link to="/products" className="text-sm font-semibold text-primary">
            Add products
          </Link>
        </div>
        <div className="mt-4 space-y-3">
          {subscriptions.map((sub) => (
            <div key={sub.id} className="rounded-xl border border-[#EAEAEA] bg-white p-4">
              <div className="flex flex-wrap items-center justify-between gap-3">
                <div>
                  <p className="font-semibold text-black">{sub.product_name}</p>
                  <p className="text-sm text-[#333333]">
                    {sub.frequency} | Qty {sub.quantity} | {sub.status}
                  </p>
                  <p className="text-sm text-[#333333]">
                    Start {sub.start_date} | End {sub.estimated_end_date}
                  </p>
                </div>
                <div className="flex gap-2">
                  {sub.status === "ACTIVE" && <span className="badge-primary">Active</span>}
                  {sub.status === "ACTIVE" ? (
                    <button onClick={() => updateSubStatus(sub.id, "pause")} className="pill-btn">
                      Pause
                    </button>
                  ) : (
                    <button onClick={() => updateSubStatus(sub.id, "resume")} className="pill-btn">
                      Resume
                    </button>
                  )}
                  <button onClick={() => updateSubStatus(sub.id, "cancel")} className="btn-dark px-3 py-1.5 text-xs">
                    Cancel
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      </section>

      <section className="grid gap-4 lg:grid-cols-2">
        <div className="card-surface p-5">
          <h3 className="font-serif text-xl text-black">Payment History</h3>
          <div className="mt-3 space-y-2">
            {payments.map((payment) => (
              <p key={payment.id} className="rounded-xl border border-[#EAEAEA] p-3 text-sm text-[#333333]">
                {payment.transaction_id} - Rs {payment.amount} ({payment.status})
              </p>
            ))}
          </div>
          <Link to="/payment" className="mt-3 inline-block text-sm font-semibold text-primary">
            Open payment page
          </Link>
        </div>

        <div className="card-surface p-5">
          <h3 className="font-serif text-xl text-black">Address Management</h3>
          <textarea
            value={address}
            onChange={(event) => setAddress(event.target.value)}
            className="input-field mt-3 min-h-28"
            placeholder="Update your delivery address"
          />
          <button onClick={saveAddress} className="btn-primary mt-3 rounded-xl px-4 py-2 text-sm">
            Save Address
          </button>
        </div>
      </section>

      <section className="card-surface p-5">
        <h3 className="font-serif text-xl text-black">One Time Orders</h3>
        <div className="mt-3 space-y-2">
          {orders.map((order) => (
            <div key={order.id} className="rounded-xl border border-[#EAEAEA] p-3 text-sm text-[#333333]">
              Order #{order.id} - Rs {order.total_amount} ({order.status})
            </div>
          ))}
        </div>
      </section>
    </main>
  );
}

function Metric({ title, value }) {
  return (
    <div className="card-surface p-4">
      <p className="text-xs uppercase tracking-wide text-[#333333]">{title}</p>
      <p className="mt-2 text-3xl font-bold text-black">{value}</p>
    </div>
  );
}

export default CustomerDashboard;
