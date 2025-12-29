import React, { useEffect, useState } from 'react';
import api from '../api/client';
import { useAuth } from '../hooks/useAuth';
import { buildImageUrl } from '../utils/imageUrl';

const AccountPage = () => {
  const { user, refreshUser, logout } = useAuth();
  const [form, setForm] = useState({
    username: '',
    email: '',
    first_name: '',
    last_name: '',
  });
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState('');
  const [avatar, setAvatar] = useState(null);
  const [avatarPreview, setAvatarPreview] = useState(null);

  useEffect(() => {
    if (user) {
      setForm({
        username: user.username || '',
        email: user.email || '',
        first_name: user.first_name || '',
        last_name: user.last_name || '',
      });
    }
  }, [user]);

  useEffect(() => {
    // Load current profile avatar
    api
      .get('/auth/profile/')
      .then((res) => {
        if (res.data.avatar) {
          setAvatarPreview(buildImageUrl(res.data.avatar));
        }
      })
      .catch(() => {
        // ignore
      });
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSaving(true);
    setMessage('');
    try {
      await api.patch('/auth/me/', form);
      if (avatar) {
        const formData = new FormData();
        formData.append('avatar', avatar);
        await api.patch('/auth/profile/', formData, {
          headers: { 'Content-Type': 'multipart/form-data' },
        });
      }
      await refreshUser();
      setMessage('Account details updated');
    } catch (err) {
      setMessage('Could not update account. Please try again.');
    } finally {
      setSaving(false);
    }
  };

  if (!user) return null;

  return (
    <div className="page-container">
      <div className="account-layout">
        <div className="account-main card">
          <h1 className="section-title">Your Account</h1>
          <p className="account-subtitle">Manage your profile information</p>

          <div className="account-avatar-section">
            <div className="account-avatar-wrapper">
              {avatarPreview ? (
                <img src={avatarPreview} alt={user.username} className="account-avatar" />
              ) : (
                <div className="account-avatar placeholder">
                  <span>{user.username?.charAt(0).toUpperCase()}</span>
                </div>
              )}
            </div>
            <div>
              <label htmlFor="avatar">Profile photo</label>
              <input
                id="avatar"
                name="avatar"
                type="file"
                accept="image/*"
                onChange={(e) => {
                  const file = e.target.files?.[0];
                  if (!file) return;
                  setAvatar(file);
                  setAvatarPreview(URL.createObjectURL(file));
                }}
              />
            </div>
          </div>

          <form onSubmit={handleSubmit} className="account-form">
            <div>
              <label htmlFor="username">Username</label>
              <input
                id="username"
                name="username"
                value={form.username}
                onChange={handleChange}
              />
            </div>

            <div>
              <label htmlFor="email">Email</label>
              <input
                id="email"
                name="email"
                type="email"
                value={form.email}
                onChange={handleChange}
              />
            </div>

            <div className="account-form-row">
              <div>
                <label htmlFor="first_name">First name</label>
                <input
                  id="first_name"
                  name="first_name"
                  value={form.first_name}
                  onChange={handleChange}
                />
              </div>

              <div>
                <label htmlFor="last_name">Last name</label>
                <input
                  id="last_name"
                  name="last_name"
                  value={form.last_name}
                  onChange={handleChange}
                />
              </div>
            </div>

            {message && <p className="account-message">{message}</p>}

            <div className="account-actions">
              <button
                type="submit"
                className="btn-primary"
                disabled={saving}
              >
                {saving ? 'Saving...' : 'Save changes'}
              </button>
            </div>
          </form>
        </div>

        <div className="account-side card">
          <h2 className="section-title">Security</h2>
          <p className="account-subtitle">
            For password changes, use the reset flow or ask an admin.
          </p>
          <button type="button" className="btn-ghost" onClick={logout}>
            Sign out
          </button>
        </div>
      </div>
    </div>
  );
};

export default AccountPage;
