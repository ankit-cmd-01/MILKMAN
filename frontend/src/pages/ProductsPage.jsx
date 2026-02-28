import { useCallback, useEffect, useState } from "react";
import { Link } from "react-router-dom";

import ProductCard from "../components/ProductCard";
import SubscribeModal from "../components/SubscribeModal";
import { cartApi, productApi } from "../api/services";
import { useAuth } from "../context/AuthContext";
import { useToast } from "../context/ToastContext";

function ProductsPage() {
  const { isAuthenticated, setIsLoginModalOpen } = useAuth();
  const { pushToast } = useToast();
  const [products, setProducts] = useState([]);
  const [categories, setCategories] = useState([]);
  const [search, setSearch] = useState("");
  const [category, setCategory] = useState("");
  const [selectedProduct, setSelectedProduct] = useState(null);

  const loadProducts = useCallback(async () => {
    const params = {};
    if (search) params.search = search;
    if (category) params.category = category;
    const response = await productApi.list(params);
    setProducts(productApi.normalizeList(response.data));
  }, [search, category]);

  useEffect(() => {
    Promise.all([loadProducts(), productApi.categories()])
      .then(([, categoryResponse]) => {
        const data = categoryResponse.data?.results || categoryResponse.data;
        setCategories(Array.isArray(data) ? data : []);
      })
      .catch(() => pushToast("Unable to load products.", "error"));
  }, [loadProducts, pushToast]);

  const handleSearch = async (event) => {
    event.preventDefault();
    try {
      await loadProducts();
    } catch {
      pushToast("Search failed.", "error");
    }
  };

  const handleAddToCart = async (product) => {
    if (!isAuthenticated) {
      setIsLoginModalOpen(true);
      return;
    }
    try {
      await cartApi.add(product.id, 1);
      pushToast(`${product.name} added to cart.`, "success");
    } catch (error) {
      pushToast(error.response?.data?.detail || "Unable to add to cart.", "error");
    }
  };

  const handleSubscribe = (product) => {
    if (!isAuthenticated) {
      setIsLoginModalOpen(true);
      return;
    }
    setSelectedProduct(product);
  };

  return (
    <main className="mx-auto max-w-7xl px-4 py-8 md:px-6">
      <div className="card-surface p-4">
        <form onSubmit={handleSearch} className="grid gap-3 md:grid-cols-[1fr_220px_auto]">
          <input
            type="text"
            value={search}
            onChange={(event) => setSearch(event.target.value)}
            placeholder="Search by product name"
            className="input-field"
          />
          <select value={category} onChange={(event) => setCategory(event.target.value)} className="input-field">
            <option value="">All Categories</option>
            {categories.map((item) => (
              <option key={item.id} value={item.id}>
                {item.name}
              </option>
            ))}
          </select>
          <button type="submit" className="btn-primary px-5 py-2 text-sm">
            Filter
          </button>
        </form>
      </div>

      <div className="mt-6 grid gap-5 sm:grid-cols-2 lg:grid-cols-4">
        {products.map((product) => (
          <ProductCard key={product.id} product={product} onAddToCart={handleAddToCart} onSubscribe={handleSubscribe} />
        ))}
      </div>

      <section className="card-surface mt-10 p-5">
        <h3 className="font-serif text-2xl text-black">One Time Orders</h3>
        <p className="mt-1 text-sm text-[#333333]">
          Add up to 5 dairy products in cart and checkout instantly.
        </p>
        <Link to="/cart" className="btn-primary mt-4 inline-block rounded-xl px-5 py-2 text-sm">
          Go to Cart Checkout
        </Link>
      </section>

      {selectedProduct && (
        <SubscribeModal product={selectedProduct} onClose={() => setSelectedProduct(null)} onSubscribed={loadProducts} />
      )}
    </main>
  );
}

export default ProductsPage;
