import React, { useEffect, useState } from 'react';
import api from '../api/client';

const OrderHistoryPage = () => {
  const [orders, setOrders] = useState([]);

  useEffect(() => {
    api.get('/orders/').then((res) => setOrders(res.data));
  }, []);

  return (
    <div className="page-container">
      <h1 className="section-title">Your Orders</h1>
      {orders.length === 0 && <p>No past orders.</p>}
      <div className="orders-list">
        {orders.map((order) => (
          <div key={order.id} className="card order-card">
            <div className="order-card-header">
              <div>
                <h3>Order #{order.id}</h3>
                {order.created_at && (
                  <p className="order-date">
                    Placed on {new Date(order.created_at).toLocaleDateString()}
                  </p>
                )}
              </div>
              <span className={`order-status order-status-${order.status}`}>
                {order.status}
              </span>
            </div>
            <p className="order-total">Total: ${order.total_price}</p>
            <ul className="order-items">
              {order.order_items.map((item) => (
                <li key={item.id} className="order-item">
                  <span className="order-item-name">{item.product.name}</span>
                  <span className="order-item-meta">
                    Qty {item.quantity} · ${item.price_at_purchase} each
                  </span>
                </li>
              ))}
            </ul>
          </div>
        ))}
      </div>
    </div>
  );
};

export default OrderHistoryPage;
