import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import ProductCard from "../components/ProductCard";
import SubscribeModal from "../components/SubscribeModal";
import { productApi, cartApi } from "../api/services";
import { useAuth } from "../context/AuthContext";
import { useToast } from "../context/ToastContext";

function HomePage() {
  const { isAuthenticated, setIsLoginModalOpen } = useAuth();
  const { pushToast } = useToast();
  const [products, setProducts] = useState([]);
  const [selectedProduct, setSelectedProduct] = useState(null);

  useEffect(() => {
    const loadFeatured = async () => {
      const response = await productApi.list({ ordering: "-demand_count" });
      setProducts(productApi.normalizeList(response.data).slice(0, 4));
    };
    loadFeatured().catch(() => pushToast("Unable to load products.", "error"));
  }, [pushToast]);

  const handleAddToCart = async (product) => {
    if (!isAuthenticated) {
      setIsLoginModalOpen(true);
      return;
    }
    try {
      await cartApi.add(product.id, 1);
      pushToast(`${product.name} added to cart.`, "success");
    } catch {
      pushToast("Failed to add item to cart.", "error");
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
    <main>
      <section className="border-b border-[#EAEAEA] bg-white">
        <div className="mx-auto grid max-w-7xl gap-8 px-4 py-14 md:grid-cols-2 md:px-6 md:py-20">
          <div className="space-y-5">
            <p className="inline-flex rounded-full border border-lightBrown px-3 py-1 text-xs font-semibold tracking-wider text-lightBrown">
              FARM TO HOME
            </p>
            <h1 className="font-serif text-4xl font-bold leading-tight text-black md:text-5xl">
              Fresh Dairy Delivered Daily
            </h1>
            <p className="max-w-xl text-[#333333]">
              Premium Indian dairy essentials crafted for families who value freshness, purity, and reliability. At Milk Man, we deliver quality dairy products to your doorstep through flexible daily and weekly subscriptions designed for modern living. Our commitment is simple, consistent quality, trusted service, and complete customer satisfaction.

– Founder Ankit Shinde
            </p>
            <div className="flex flex-wrap gap-3">
              <Link to="/products" className="btn-primary rounded-xl px-5 py-2.5 text-sm">
                Explore Dairy Products
              </Link>
              <Link to="/subscription-plans" className="btn-secondary rounded-xl px-5 py-2.5 text-sm">
                View Subscription Plans
              </Link>
            </div>
          </div>
          <div className="card-surface overflow-hidden rounded-xl">
            <img
              src="https://nutritionsource.hsph.harvard.edu/wp-content/uploads/2024/11/AdobeStock_354060824-1024x683.jpeg"
              alt="Fresh dairy"
              className="h-full w-full object-cover"
            />
          </div>
        </div>
      </section>

      <section className="mx-auto max-w-7xl px-4 py-12 md:px-6">
        <div className="mb-6 flex items-center justify-between">
          <h2 className="font-serif text-3xl font-semibold text-black">Featured Products</h2>
          <Link to="/products" className="text-sm font-semibold text-primary">
            See all
          </Link>
        </div>
        <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-4">
          {products.map((product) => (
            <ProductCard
              key={product.id}
              product={product}
              onAddToCart={handleAddToCart}
              onSubscribe={handleSubscribe}
            />
          ))}
        </div>
      </section>

      {selectedProduct && (
        <SubscribeModal
          product={selectedProduct}
          onClose={() => setSelectedProduct(null)}
          onSubscribed={() => setSelectedProduct(null)}
        />
      )}
    </main>
  );
}

export default HomePage;
