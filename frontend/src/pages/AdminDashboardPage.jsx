import React, { useEffect, useState } from 'react';
import api from '../api/client';

const AdminDashboardPage = () => {
  const [products, setProducts] = useState([]);
  const [orders, setOrders] = useState([]);

  const load = () => {
    api.get('/products/').then((res) => setProducts(res.data));
    api.get('/orders/').then((res) => setOrders(res.data));
  };

  useEffect(() => {
    load();
  }, []);

  const updateOrderStatus = async (id, status) => {
    await api.patch(`/orders/${id}/`, { status });
    load();
  };

  return (
    <div className="page-container">
      <h1>Admin Dashboard</h1>

      <section>
        <h2>Products</h2>
        {products.map((p) => (
          <div key={p.id} className="card" style={{ marginBottom: '0.5rem' }}>
            <strong>{p.name}</strong> - Stock: {p.stock_quantity} - Price: {p.final_price}
          </div>
        ))}
      </section>

      <section>
        <h2>Orders</h2>
        {orders.map((order) => (
          <div key={order.id} className="card" style={{ marginBottom: '0.5rem' }}>
            <p>
              Order #{order.id} - {order.status} - Total: {order.total_price}
            </p>
            <button type="button" onClick={() => updateOrderStatus(order.id, 'shipped')}>
              Mark Shipped
            </button>
            <button type="button" onClick={() => updateOrderStatus(order.id, 'delivered')}>
              Mark Delivered
            </button>
            <button type="button" onClick={() => updateOrderStatus(order.id, 'cancelled')}>
              Cancel
            </button>
          </div>
        ))}
      </section>
    </div>
  );
};

export default AdminDashboardPage;
