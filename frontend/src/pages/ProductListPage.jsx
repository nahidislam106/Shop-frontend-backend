import React, { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';
import api from '../api/client';
import ProductCard from '../components/ProductCard';

const ProductListPage = () => {
  const location = useLocation();
  const [products, setProducts] = useState([]);
  const [filter, setFilter] = useState('all');
  const [sort, setSort] = useState('featured');
  const [searchTerm, setSearchTerm] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const params = new URLSearchParams(location.search);
    setSearchTerm(params.get('q') || '');
  }, [location.search]);

  useEffect(() => {
    setLoading(true);
    api
      .get('/products/', {
        params: {
          filter,
          sort,
          q: searchTerm || undefined,
        },
      })
      .then((res) => setProducts(res.data))
      .finally(() => setLoading(false));
  }, [filter, sort, searchTerm]);

  const setFilterAndSort = (nextFilter, nextSort = sort) => {
    setFilter(nextFilter);
    setSort(nextSort);
  };

  return (
    <div className="page-container">
      <div className="hero-banner">
        <div>
          <div className="hero-title">Welcome to ShopPrime</div>
          <div className="hero-subtitle">
            Discover hand-picked tech, fashion, and home essentials with fast delivery and exclusive
            deals.
          </div>
          <div className="hero-pill">
            <span>★</span>
            <span>Members get early access to big sales</span>
          </div>
        </div>
        <button
          type="button"
          className="hero-cta"
          onClick={() => setFilterAndSort('deals')}
        >
          View today&apos;s deals
        </button>
      </div>

      {searchTerm && (
        <div style={{ marginBottom: '0.75rem', fontSize: '0.9rem', color: '#4b5563' }}>
          Showing results for <strong>{searchTerm}</strong>
        </div>
      )}

      <div className="filters-row">
        <div className="filter-chips">
          <button
            type="button"
            className={`chip ${filter === 'all' ? 'chip--primary' : ''}`}
            onClick={() => setFilterAndSort('all')}
          >
            All
          </button>
          <button
            type="button"
            className={`chip ${filter === 'best' ? 'chip--primary' : ''}`}
            onClick={() => setFilterAndSort('best')}
          >
            Best Sellers
          </button>
          <button
            type="button"
            className={`chip ${filter === 'new' ? 'chip--primary' : ''}`}
            onClick={() => setFilterAndSort('new', 'newest')}
          >
            New Arrivals
          </button>
          <button
            type="button"
            className={`chip ${filter === 'deals' ? 'chip--primary' : ''}`}
            onClick={() => setFilterAndSort('deals')}
          >
            Deals
          </button>
        </div>
        <select
          className="sort-select"
          value={sort}
          onChange={(e) => setSort(e.target.value)}
        >
          <option value="featured">Sort by: Featured</option>
          <option value="price_low">Price: Low to High</option>
          <option value="price_high">Price: High to Low</option>
          <option value="newest">Newest</option>
        </select>
      </div>

      <div className="card-grid">
        {loading && <div>Loading products...</div>}
        {!loading && products.length === 0 && <div>No products found.</div>}
        {!loading &&
          products.map((p) => (
            <ProductCard key={p.id} product={p} />
          ))}
      </div>
    </div>
  );
};

export default ProductListPage;
