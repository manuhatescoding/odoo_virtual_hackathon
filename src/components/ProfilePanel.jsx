import { useEffect, useState } from 'react';
import axios from 'axios';
import './workspace-panels.css';

export default function ProfilePanel({ user }) {
  const [profile, setProfile] = useState({ name: user.full_name, job_title: user.role === 'admin' ? 'HR Administrator' : 'Employee', department: 'People Operations', phone: '', address: '', profile_picture: '' });
  const [editing, setEditing] = useState(false);
  const [message, setMessage] = useState('');
  useEffect(() => { axios.get('/api/employees/me/profile').then((response) => setProfile(response.data)).catch(() => setMessage('Profile could not be loaded')); }, []);
  const update = async (event) => { event.preventDefault(); try { const response = await axios.patch('/api/employees/me/profile', { phone: profile.phone, address: profile.address, profile_picture: profile.profile_picture }); setProfile(response.data); setEditing(false); setMessage('Profile updated'); } catch (error) { setMessage(error.response?.data?.detail || 'Profile could not be updated'); } };
  return <section className="panel full-panel profile-panel"><div className="panel-heading"><div><h2>My profile</h2><p className="muted">View and manage your personal details.</p></div><button className="secondary-button" onClick={() => setEditing(!editing)}>{editing ? 'Cancel' : 'Edit profile'}</button></div>{message && <p className="live-status">{message}</p>}{editing ? <form className="profile-form" onSubmit={update}><label>Phone<input value={profile.phone || ''} onChange={(event) => setProfile({ ...profile, phone: event.target.value })} /></label><label>Address<input value={profile.address || ''} onChange={(event) => setProfile({ ...profile, address: event.target.value })} /></label><label>Profile picture URL<input value={profile.profile_picture || ''} onChange={(event) => setProfile({ ...profile, profile_picture: event.target.value })} /></label><button className="primary-button">Save profile</button></form> : <div className="profile-summary"><div className="avatar large">{profile.name?.slice(0, 2).toUpperCase()}</div><div><h3>{profile.name}</h3><p className="muted">{profile.job_title} - {profile.department}</p><p className="muted">{profile.phone || 'No phone number added'} - {profile.address || 'No address added'}</p></div></div>}</section>;
}
