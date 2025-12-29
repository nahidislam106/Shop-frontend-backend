import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import api from '../api/client';
import { buildImageUrl } from '../utils/imageUrl';

const ProductDetailPage = () => {
  const { id } = useParams();
  const [product, setProduct] = useState(null);
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    setLoading(true);
    api
      .get(`/products/${id}/`)
      .then((res) => setProduct(res.data))
      .finally(() => setLoading(false));
  }, [id]);

  const addToCart = async () => {
    await api.post('/cart/add/', { product_id: product.id, quantity: 1 });
    setMessage('Added to cart');
  };

  if (loading || !product) return <div className="page-container">Loading...</div>;

  const hasDiscount = Number(product.discount_percentage) > 0;

  return (
    <div className="page-container">
      <div className="product-detail">
        <div className="product-detail-main">
          {product.image && (
            <img
              className="product-detail-image"
              src={buildImageUrl(product.image)}
              alt={product.name}
            />
          )}
          <h1 className="section-title">{product.name}</h1>
          <p className="product-detail-description">{product.description}</p>
        </div>

        <aside className="product-detail-sidebar">
          <div className="price-row">
            <span className="price-main">${product.final_price}</span>
            {hasDiscount && <span className="price-strike">${product.price}</span>}
          </div>
          {hasDiscount && <span className="badge-deal">Limited-time deal</span>}
          <div className="badge-prime">
            <span>✓</span>
            <span>Fast delivery available</span>
          </div>
          <p style={{ fontSize: '0.85rem', marginTop: '0.75rem' }}>
            {product.is_available
              ? `In stock (${product.stock_quantity} available)`
              : 'Currently out of stock'}
          </p>

          <button
            type="button"
            className="btn-primary"
            onClick={addToCart}
            disabled={!product.is_available}
            style={{ marginTop: '0.9rem', width: '100%' }}
          >
            {product.is_available ? 'Add to Cart' : 'Out of Stock'}
          </button>

          {message && (
            <p style={{ marginTop: '0.5rem', fontSize: '0.85rem', color: '#16a34a' }}>{message}</p>
          )}
        </aside>
      </div>
    </div>
  );
};

export default ProductDetailPage;
