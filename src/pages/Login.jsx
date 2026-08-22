import { useState } from 'react';
import { login } from '../services/authService';

export default function Login({ onLogin }) {
  const [username, setUsername] = useState('admin');
  const [password, setPassword] = useState('admin123');
  const submit = async (event) => { event.preventDefault(); const { data } = await login({ username, password }); onLogin?.(data.user); };
  return <form onSubmit={submit}><input value={username} onChange={(event) => setUsername(event.target.value)} /><input type="password" value={password} onChange={(event) => setPassword(event.target.value)} /><button>Sign in</button></form>;
}
