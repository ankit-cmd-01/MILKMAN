import { useMemo, useState } from "react";

import { subscriptionApi } from "../api/services";
import { useToast } from "../context/ToastContext";

const DEFAULT_DAYS = 30;

function SubscribeModal({ product, onClose, onSubscribed }) {
  const { pushToast } = useToast();
  const today = new Date().toISOString().split("T")[0];
  const [quantity, setQuantity] = useState(1);
  const [frequency, setFrequency] = useState("DAILY");
  const [startDate, setStartDate] = useState(today);
  const [endDate, setEndDate] = useState("");
  const [loading, setLoading] = useState(false);

  const computed = useMemo(() => {
    const start = new Date(startDate);
    const effectiveEnd = endDate ? new Date(endDate) : new Date(start.getTime() + (DEFAULT_DAYS - 1) * 86400000);
    const days = Math.max(1, Math.floor((effectiveEnd - start) / 86400000) + 1);
    const deliveries = frequency === "WEEKLY" ? Math.ceil(days / 7) : days;
    const total = deliveries * quantity * Number(product.price || 0);
    return {
      estimatedEndDate: effectiveEnd.toISOString().split("T")[0],
      total,
    };
  }, [startDate, endDate, quantity, frequency, product.price]);

  const handleSubmit = async (event) => {
    event.preventDefault();
    setLoading(true);
    try {
      const payload = {
        product: product.id,
        quantity,
        frequency,
        start_date: startDate,
      };
      if (endDate) payload.end_date = endDate;
      await subscriptionApi.create(payload);
      pushToast("Subscription created successfully.", "success");
      onSubscribed?.();
      onClose();
    } catch (error) {
      pushToast(error.response?.data?.detail || "Unable to create subscription.", "error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/45 px-4">
      <div className="modal-panel w-full max-w-xl p-6">
        <div className="mb-4 flex items-center justify-between">
          <h3 className="font-serif text-2xl font-bold text-black">Subscribe: {product.name}</h3>
          <button onClick={onClose} className="text-xl text-[#333333]">
            x
          </button>
        </div>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid gap-3 sm:grid-cols-2">
            <label className="text-sm text-[#333333]">
              Frequency
              <div className="mt-1 grid grid-cols-2 gap-2">
                <button
                  type="button"
                  onClick={() => setFrequency("DAILY")}
                  className={`rounded-xl px-3 py-2 text-sm font-semibold transition ${
                    frequency === "DAILY"
                      ? "bg-primary text-white"
                      : "border border-[#EAEAEA] bg-white text-[#333333]"
                  }`}
                >
                  Daily
                </button>
                <button
                  type="button"
                  onClick={() => setFrequency("WEEKLY")}
                  className={`rounded-xl px-3 py-2 text-sm font-semibold transition ${
                    frequency === "WEEKLY"
                      ? "bg-primary text-white"
                      : "border border-[#EAEAEA] bg-white text-[#333333]"
                  }`}
                >
                  Weekly
                </button>
              </div>
            </label>
            <label className="text-sm text-[#333333]">
              Quantity
              <input
                type="number"
                min="1"
                value={quantity}
                onChange={(e) => setQuantity(Number(e.target.value) || 1)}
                className="input-field mt-1"
              />
            </label>
          </div>
          <div className="grid gap-3 sm:grid-cols-2">
            <label className="text-sm text-[#333333]">
              Start date
              <input type="date" value={startDate} onChange={(e) => setStartDate(e.target.value)} className="input-field mt-1" />
            </label>
            <label className="text-sm text-[#333333]">
              End date (optional)
              <input type="date" value={endDate} onChange={(e) => setEndDate(e.target.value)} className="input-field mt-1" />
            </label>
          </div>

          <div className="rounded-xl border border-lightBrown bg-white p-4 text-sm text-black">
            <p>
              Estimated end date: <strong>{computed.estimatedEndDate}</strong>
            </p>
            <p>
              Dynamic total amount: <strong className="text-lightBrown">Rs {computed.total.toFixed(2)}</strong>
            </p>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="btn-primary w-full px-4 py-2.5 text-sm"
          >
            {loading ? "Creating..." : "Confirm Subscription"}
          </button>
        </form>
      </div>
    </div>
  );
}

export default SubscribeModal;
