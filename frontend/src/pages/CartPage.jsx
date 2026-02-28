import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import { cartApi } from "../api/services";
import { useToast } from "../context/ToastContext";

function CartPage() {
  const navigate = useNavigate();
  const { pushToast } = useToast();
  const [cart, setCart] = useState(null);
  const [paymentMethod, setPaymentMethod] = useState("UPI");
  const [loading, setLoading] = useState(false);

  const loadCart = async () => {
    const response = await cartApi.detail();
    setCart(response.data);
  };

  useEffect(() => {
    loadCart().catch(() => pushToast("Unable to load cart.", "error"));
  }, [pushToast]);

  const updateQty = async (itemId, quantity) => {
    try {
      await cartApi.update(itemId, quantity);
      await loadCart();
    } catch (error) {
      pushToast(error.response?.data?.detail || "Update failed.", "error");
    }
  };

  const removeItem = async (itemId) => {
    await cartApi.remove(itemId);
    await loadCart();
    pushToast("Item removed.", "success");
  };

  const checkout = async () => {
    setLoading(true);
    try {
      const response = await cartApi.checkout(paymentMethod);
      pushToast("Order created. Proceed to payment.", "success");
      navigate("/payment", { state: response.data });
    } catch (error) {
      pushToast(error.response?.data?.detail || "Checkout failed.", "error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="mx-auto max-w-5xl px-4 py-8 md:px-6">
      <h1 className="font-serif text-3xl font-bold text-black">Cart</h1>
      <p className="mt-1 text-sm text-[#333333]">One Time Orders: up to 5 products</p>

      <div className="mt-6 space-y-3">
        {cart?.items?.length ? (
          cart.items.map((item) => (
            <div key={item.id} className="card-surface flex flex-wrap items-center justify-between gap-3 p-4">
              <div>
                <p className="font-semibold text-black">{item.product_name}</p>
                <p className="text-sm text-[#333333]">Rs {item.unit_price} each</p>
              </div>
              <div className="flex items-center gap-2">
                <input
                  type="number"
                  min="1"
                  value={item.quantity}
                  onChange={(event) => updateQty(item.id, Number(event.target.value) || 1)}
                  className="input-field w-20"
                />
                <button onClick={() => removeItem(item.id)} className="btn-secondary px-3 py-2 text-sm">
                  Remove
                </button>
              </div>
            </div>
          ))
        ) : (
          <div className="rounded-xl border border-dashed border-[#EAEAEA] bg-white p-6 text-sm text-[#333333]">
            Cart is empty.
          </div>
        )}
      </div>

      <div className="card-surface mt-6 p-5">
        <p className="text-lg font-semibold text-black">
          Total: <span className="text-lightBrown">Rs {cart?.total_value || "0.00"}</span>
        </p>
        <div className="mt-3 flex flex-wrap items-center gap-3">
          <select value={paymentMethod} onChange={(event) => setPaymentMethod(event.target.value)} className="input-field max-w-56">
            <option value="UPI">UPI</option>
            <option value="CARD">Card</option>
            <option value="NET_BANKING">Net Banking</option>
            <option value="CASH">Cash</option>
          </select>
          <button
            disabled={loading || !cart?.items?.length}
            onClick={checkout}
            className="btn-primary rounded-xl px-5 py-2 text-sm disabled:opacity-50"
          >
            {loading ? "Processing..." : "Proceed to Payment"}
          </button>
        </div>
      </div>
    </main>
  );
}

export default CartPage;
