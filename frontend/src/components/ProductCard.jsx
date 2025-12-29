import React from 'react';
import { Link } from 'react-router-dom';
import api from '../api/client';
import { buildImageUrl } from '../utils/imageUrl';

const ProductCard = ({ product }) => {
  const handleAddToCart = async () => {
    try {
      await api.post('/cart/add/', { product_id: product.id, quantity: 1 });
      // Simple feedback; could be replaced by a toast system later.
      // eslint-disable-next-line no-alert
      alert('Added to cart');
    } catch (e) {
      // eslint-disable-next-line no-alert
      alert('Please sign in to add items to your cart.');
    }
  };

  const hasDiscount = Number(product.discount_percentage) > 0;

  return (
    <div className="card">
      {product.image && (
        <img
          src={buildImageUrl(product.image)}
          alt={product.name}
          style={{ width: '100%', objectFit: 'cover' }}
        />
      )}
      <div style={{ flex: 1 }}>
        <h3>{product.name}</h3>
        {product.description && (
          <p style={{ fontSize: '0.85rem', color: '#4b5563', marginTop: '0.2rem' }}>
            {product.description.length > 90
              ? `${product.description.slice(0, 90)}...`
              : product.description}
          </p>
        )}

        <div className="price-row">
          <span className="price-main">${product.final_price}</span>
          {hasDiscount && <span className="price-strike">${product.price}</span>}
        </div>

        {hasDiscount && <span className="badge-deal">Limited-time deal</span>}
        <div className="badge-prime">
          <span>✓</span>
          <span>Fast delivery</span>
        </div>
      </div>

      <div style={{ display: 'flex', gap: '0.5rem', marginTop: '0.7rem' }}>
        <button type="button" className="btn-primary" onClick={handleAddToCart}>
          Add to Cart
        </button>
        <Link to={`/products/${product.id}`} className="btn-ghost">
          View
        </Link>
      </div>
    </div>
  );
};

export default ProductCard;
