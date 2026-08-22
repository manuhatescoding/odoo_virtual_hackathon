import axios from 'axios';

export const login = (credentials) => axios.post('/api/auth/login', credentials);
export const register = (userData) => axios.post('/api/auth/register', userData);
export const logout = () => { localStorage.removeItem('dayflow_user'); localStorage.removeItem('dayflow_token'); };
export default { login, register, logout };
