import { useState } from "react";

import { useAuth } from "../context/AuthContext";
import { useToast } from "../context/ToastContext";

function LoginModal() {
  const { isLoginModalOpen, setIsLoginModalOpen, login, register } = useAuth();
  const { pushToast } = useToast();
  const [tab, setTab] = useState("login");
  const [loading, setLoading] = useState(false);
  const [form, setForm] = useState({
    email: "",
    password: "",
    confirm_password: "",
    first_name: "",
    last_name: "",
    phone_number: "",
    address: "",
  });

  if (!isLoginModalOpen) return null;

  const handleChange = (event) => {
    setForm((prev) => ({ ...prev, [event.target.name]: event.target.value }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setLoading(true);
    try {
      if (tab === "login") {
        await login(form.email, form.password);
        pushToast("Login successful.", "success");
      } else {
        await register(form);
        pushToast("Registration successful. Please login.", "success");
        setTab("login");
      }
    } catch (error) {
      const detail = error.response?.data?.detail || "Authentication failed.";
      pushToast(detail, "error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/45 px-4">
      <div className="modal-panel w-full max-w-lg p-6">
        <div className="mb-4 flex items-center justify-between">
          <h2 className="font-serif text-2xl font-bold text-black">
            {tab === "login" ? "Login to MilkMan" : "Create Account"}
          </h2>
          <button onClick={() => setIsLoginModalOpen(false)} className="text-xl text-[#333333]">
            x
          </button>
        </div>

        <div className="mb-4 flex rounded-xl border border-[#EAEAEA] p-1">
          <button
            type="button"
            onClick={() => setTab("login")}
            className={`flex-1 rounded-lg py-2 text-sm font-semibold transition ${tab === "login" ? "bg-primary text-white" : "text-[#333333]"}`}
          >
            Login
          </button>
          <button
            type="button"
            onClick={() => setTab("register")}
            className={`flex-1 rounded-lg py-2 text-sm font-semibold transition ${tab === "register" ? "bg-primary text-white" : "text-[#333333]"}`}
          >
            Register
          </button>
        </div>

        <form onSubmit={handleSubmit} className="space-y-3">
          <input
            name="email"
            type="email"
            placeholder="Email"
            value={form.email}
            onChange={handleChange}
            className="input-field"
            required
          />
          <input
            name="password"
            type="password"
            placeholder="Password"
            value={form.password}
            onChange={handleChange}
            className="input-field"
            required
          />

          {tab === "register" && (
            <>
              <input
                name="confirm_password"
                type="password"
                placeholder="Confirm password"
                value={form.confirm_password}
                onChange={handleChange}
                className="input-field"
                required
              />
              <div className="grid gap-3 sm:grid-cols-2">
                <input
                  name="first_name"
                  placeholder="First name"
                  value={form.first_name}
                  onChange={handleChange}
                  className="input-field"
                />
                <input
                  name="last_name"
                  placeholder="Last name"
                  value={form.last_name}
                  onChange={handleChange}
                  className="input-field"
                />
              </div>
              <input
                name="phone_number"
                placeholder="Phone number"
                value={form.phone_number}
                onChange={handleChange}
                className="input-field"
              />
              <textarea
                name="address"
                placeholder="Address"
                value={form.address}
                onChange={handleChange}
                className="input-field min-h-20"
              />
            </>
          )}

          <button
            type="submit"
            disabled={loading}
            className="btn-primary w-full px-4 py-2.5 text-sm"
          >
            {loading ? "Please wait..." : tab === "login" ? "Login" : "Create account"}
          </button>
        </form>

        <p className="mt-4 text-xs text-[#333333]">
          Admin demo: <strong>ankits@gmail.com / ankit@123</strong> | Customer demo:{" "}
          <strong>customer1@test.com / strongpassword123</strong>
        </p>
      </div>
    </div>
  );
}

export default LoginModal;
