import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api/client';

const CheckoutPage = () => {
  const navigate = useNavigate();
  const [cart, setCart] = useState(null);
  const [error, setError] = useState('');

  useEffect(() => {
    api.get('/cart/me/').then((res) => setCart(res.data));
  }, []);

  const placeOrder = async () => {
    try {
      const orderItems = cart.items.map((item) => ({
        product_id: item.product.id,
        quantity: item.quantity,
      }));
      await api.post('/orders/', { order_items: orderItems });
      navigate('/orders');
    } catch (e) {
      setError('Failed to place order.');
    }
  };

  if (!cart) return <div className="page-container">Loading...</div>;

  return (
    <div className="page-container">
      <h1>Checkout</h1>
      <h2>Total: {cart.total_price}</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <button type="button" onClick={placeOrder} disabled={cart.items.length === 0}>
        Place Order
      </button>
    </div>
  );
};

export default CheckoutPage;
