import { Link, useLocation } from "react-router-dom";

import { useAuth } from "../context/AuthContext";

function NavLink({ to, children }) {
  const location = useLocation();
  const active = location.pathname === to;
  return (
    <Link
      to={to}
      className={`nav-link px-4 ${active ? "nav-link-active" : ""}`}
    >
      {children}
    </Link>
  );
}

function Navbar() {
  const { isAuthenticated, user, logout, setIsLoginModalOpen } = useAuth();

  return (
    <header className="sticky top-0 z-40 border-b border-[#EAEAEA] bg-white">
      <nav className="mx-auto flex max-w-7xl items-center justify-between px-4 py-3 md:px-6">
        <Link to="/" className="font-serif text-2xl font-bold tracking-wide text-black">
          MilkMan
        </Link>

        <div className="hidden items-center gap-2 md:flex">
          <NavLink to="/">Home</NavLink>
          <NavLink to="/products">Dairy Products</NavLink>
          <NavLink to="/subscription-plans">Subscription Plans</NavLink>
        </div>

        <div className="flex items-center gap-2">
          {isAuthenticated ? (
            <>
              <Link
                to={user?.role === "ADMIN" ? "/admin-dashboard" : "/customer-dashboard"}
                className="btn-secondary px-4 py-2 text-sm"
              >
                Profile
              </Link>
              <button
                type="button"
                onClick={logout}
                className="btn-primary px-4 py-2 text-sm"
              >
                Logout
              </button>
            </>
          ) : (
            <button
              type="button"
              onClick={() => setIsLoginModalOpen(true)}
              className="btn-primary px-4 py-2 text-sm"
            >
              Login
            </button>
          )}
        </div>
      </nav>
    </header>
  );
}

export default Navbar;
