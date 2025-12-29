export const buildImageUrl = (path) => {
  if (!path) return null;
  if (path.startsWith('http://') || path.startsWith('https://')) return path;

  const apiBase = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';
  const base = apiBase.replace(/\/?api\/?$/, '');

  if (path.startsWith('/')) return `${base}${path}`;
  return `${base}/${path}`;
};
