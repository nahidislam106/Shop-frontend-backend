import React, { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import api from '../api/client';
import { buildImageUrl } from '../utils/imageUrl';

const CartPage = () => {
  const navigate = useNavigate();
  const [cart, setCart] = useState(null);

  const loadCart = () => {
    api.get('/cart/me/').then((res) => setCart(res.data));
  };

  useEffect(() => {
    loadCart();
  }, []);

  const updateQuantity = async (productId, quantity) => {
    await api.post('/cart/update-quantity/', { product_id: productId, quantity });
    loadCart();
  };

  const removeItem = async (productId) => {
    await api.post('/cart/remove/', { product_id: productId });
    loadCart();
  };

  if (!cart) return <div className="page-container">Loading...</div>;

  return (
    <div className="page-container">
      <h1 className="section-title">Shopping Cart</h1>
      {cart.items.length === 0 ? (
        <p>Your cart is empty.</p>
      ) : (
        <div className="cart-layout">
          <div className="cart-items">
            {cart.items.map((item) => (
              <div key={item.id} className="card cart-item-card">
                <div className="cart-item-main">
                  {item.product.image && (
                    <img
                      src={buildImageUrl(item.product.image)}
                      alt={item.product.name}
                      className="cart-item-image"
                    />
                  )}
                  <div className="cart-item-info">
                    <h3>{item.product.name}</h3>
                    <div className="price-row">
                      <span className="price-main">${item.product.final_price}</span>
                    </div>
                    <p className="cart-item-subtotal">Subtotal: ${item.subtotal}</p>
                    <div className="cart-item-actions">
                      <div className="cart-qty-control">
                        <label htmlFor={`qty-${item.id}`}>Qty</label>
                        <input
                          id={`qty-${item.id}`}
                          type="number"
                          min="1"
                          value={item.quantity}
                          onChange={(e) =>
                            updateQuantity(item.product.id, Number(e.target.value))
                          }
                        />
                      </div>
                      <button
                        type="button"
                        className="btn-ghost"
                        onClick={() => removeItem(item.product.id)}
                      >
                        Remove
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>

          <div className="cart-summary card">
            <h2>Order Summary</h2>
            <p className="cart-summary-total">Total: ${cart.total_price}</p>
            <p className="cart-summary-items">
              {cart.items.length} item{cart.items.length > 1 ? 's' : ''} in your cart
            </p>
            <button
              type="button"
              className="btn-primary cart-summary-button"
              onClick={() => navigate('/checkout')}
            >
              Proceed to checkout
            </button>
            <p className="cart-summary-link">
              <Link to="/">Continue shopping</Link>
            </p>
          </div>
        </div>
      )}
    </div>
  );
};

export default CartPage;
