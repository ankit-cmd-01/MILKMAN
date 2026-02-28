import { Navigate } from "react-router-dom";

import { useAuth } from "../context/AuthContext";

function ProtectedRoute({ children, role }) {
  const { isAuthenticated, loading, user } = useAuth();

  if (loading) {
    return <div className="mx-auto max-w-6xl p-8 text-sm text-[#333333]">Loading...</div>;
  }

  if (!isAuthenticated) {
    return <Navigate to="/" replace />;
  }

  if (role && user?.role !== role) {
    const target = user?.role === "ADMIN" ? "/admin-dashboard" : "/customer-dashboard";
    return <Navigate to={target} replace />;
  }

  return children;
}

export default ProtectedRoute;
