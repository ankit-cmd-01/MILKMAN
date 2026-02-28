import { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";

import { paymentApi } from "../api/services";
import { useAuth } from "../context/AuthContext";
import { useToast } from "../context/ToastContext";

function PaymentPage() {
  const location = useLocation();
  const { isAdmin } = useAuth();
  const { pushToast } = useToast();
  const [payments, setPayments] = useState([]);

  const loadPayments = async () => {
    const response = await paymentApi.list();
    setPayments(paymentApi.normalizeList(response.data));
  };

  useEffect(() => {
    loadPayments().catch(() => pushToast("Unable to load payments.", "error"));
  }, [pushToast]);

  const updateStatus = async (paymentId, status) => {
    try {
      await paymentApi.updateStatus(paymentId, status);
      await loadPayments();
      pushToast("Payment status updated.", "success");
    } catch {
      pushToast("Failed to update status.", "error");
    }
  };

  return (
    <main className="mx-auto max-w-6xl px-4 py-8 md:px-6">
      <h1 className="font-serif text-3xl font-bold text-black">Payments</h1>
      {location.state?.transaction_id && (
        <p className="mt-2 rounded-xl border border-primary bg-white p-3 text-sm text-black">
          New order created. Transaction ID: <strong>{location.state.transaction_id}</strong>
        </p>
      )}

      <div className="mt-6 space-y-3">
        {payments.map((payment) => (
          <div key={payment.id} className="card-surface p-4">
            <div className="flex flex-wrap items-center justify-between gap-3">
              <div>
                <p className="font-semibold text-black">{payment.transaction_id}</p>
                <p className="text-sm text-[#333333]">
                  Amount: <span className="text-lightBrown">Rs {payment.amount}</span>
                </p>
                <p className="text-xs text-[#333333]">
                  Method: {payment.payment_method} | Status: {payment.status}
                </p>
              </div>
              {isAdmin && (
                <div className="flex gap-2">
                  <button
                    onClick={() => updateStatus(payment.id, "SUCCESS")}
                    className="btn-primary px-3 py-1.5 text-xs"
                  >
                    Mark Success
                  </button>
                  <button
                    onClick={() => updateStatus(payment.id, "FAILED")}
                    className="btn-secondary px-3 py-1.5 text-xs"
                  >
                    Mark Failed
                  </button>
                </div>
              )}
            </div>
          </div>
        ))}
      </div>
    </main>
  );
}

export default PaymentPage;
