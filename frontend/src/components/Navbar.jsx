import React, { useEffect, useState } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';

const Navbar = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { user, logout } = useAuth();

  const [search, setSearch] = useState('');

  useEffect(() => {
    const params = new URLSearchParams(location.search);
    setSearch(params.get('q') || '');
  }, [location.search]);

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    const term = search.trim();
    if (!term) {
      navigate('/');
      return;
    }
    navigate(`/?q=${encodeURIComponent(term)}`);
  };

  return (
    <nav className="navbar">
      <div className="nav-left">
        <Link to="/" className="logo">
          Shop
          <span>Prime</span>
        </Link>
      </div>

      <div className="nav-center">
        <form className="search-bar" onSubmit={handleSearchSubmit}>
          <input
            placeholder="Search for products, brands, and more"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
          <button type="submit">Search</button>
        </form>
      </div>

      <div className="nav-right">
        <div className="nav-links">
          <button
            type="button"
            className="btn-ghost nav-pill"
            onClick={() => (user ? navigate('/account') : navigate('/login'))}
          >
            <span>Hello, {user ? user.username : 'Sign in'}</span>
            <span>Account & Lists</span>
          </button>

          <button
            type="button"
            className="btn-ghost nav-cart"
            onClick={() => navigate('/cart')}
          >
            Cart
            <span className="nav-cart-badge">0</span>
          </button>

          {user?.is_superuser && (
            <button
              type="button"
              className="btn-ghost"
              onClick={() => navigate('/admin')}
            >
              Admin
            </button>
          )}

          {!user && (
            <button
              type="button"
              className="btn-primary"
              onClick={() => navigate('/login')}
            >
              Sign in
            </button>
          )}

          {user && (
            <button type="button" onClick={logout}>
              Logout
            </button>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
