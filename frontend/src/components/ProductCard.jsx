import { getProductImageByName } from "../assets/productImages";

function ProductCard({ product, onAddToCart, onSubscribe }) {
  const imageSrc = getProductImageByName(
    product.name,
    product.image_url || "https://images.unsplash.com/photo-1550583724-b2692b85b150"
  );

  return (
    <article className="card-surface group overflow-hidden">
      <div className="flex h-44 w-full items-center justify-center overflow-hidden bg-white p-3">
        <img
          src={imageSrc}
          alt={product.name}
          className="h-full w-full rounded-xl object-cover transition duration-500 group-hover:scale-105"
        />
      </div>

      <div className="space-y-2 p-4">
        <h3 className="font-serif text-xl font-semibold text-black">{product.name}</h3>
        <p className="line-clamp-2 min-h-10 text-sm text-[#333333]">{product.description || "Premium dairy product."}</p>
        <div className="flex items-center justify-between text-sm">
          <span className="font-bold text-lightBrown">Rs {product.price}</span>
          <span className="rounded-full border border-lightBrown px-2 py-1 text-xs text-lightBrown">{product.unit}</span>
        </div>
        {product.stock_warning && (
          <p className="text-xs font-medium text-lightBlueDark">{product.stock_warning}</p>
        )}
        <div className="grid grid-cols-2 gap-2 pt-1">
          <button
            type="button"
            onClick={() => onAddToCart(product)}
            className="btn-secondary px-3 py-2 text-sm"
          >
            Add to Cart
          </button>
          <button
            type="button"
            onClick={() => onSubscribe(product)}
            className="btn-primary px-3 py-2 text-sm"
          >
            Subscribe
          </button>
        </div>
      </div>
    </article>
  );
}

export default ProductCard;
