import { useEffect, useState } from 'react';
import axios from 'axios';
import Notification from './Notification';

const today = new Date().toISOString().slice(0, 10);

export default function EmployeeTools({ employee, attendance, onSaved }) {
  const [leave, setLeave] = useState({ leave_type: 'Annual', start_date: today, end_date: today, remarks: '' });
  const [message, setMessage] = useState('');
  const [profile, setProfile] = useState({ phone: employee?.phone || '', address: employee?.address || '', profile_picture: employee?.profile_picture || '' });
  const [notifications, setNotifications] = useState([]);
  const openRecord = attendance.find((record) => !record.check_out);
  const checkIn = async () => { try { await axios.post('/api/attendance', { employee_id: employee.id, check_in: new Date().toISOString(), date: today, status: 'Present' }); setMessage('Checked in successfully'); onSaved(); } catch (error) { setMessage(error.response?.data?.detail || 'Unable to check in'); } };
  const checkOut = async () => { try { await axios.patch(`/api/attendance/${openRecord.id}/checkout`); setMessage('Checked out successfully'); onSaved(); } catch (error) { setMessage(error.response?.data?.detail || 'Unable to check out'); } };
  const applyLeave = async (event) => { event.preventDefault(); try { await axios.post('/api/leave', { ...leave, employee_id: employee.id }); setMessage('Leave request submitted'); setLeave({ ...leave, remarks: '' }); onSaved(); } catch (error) { setMessage(error.response?.data?.detail || 'Unable to submit leave'); } };
  const updateProfile = async (event) => { event.preventDefault(); try { await axios.patch('/api/employees/me/profile', profile); setMessage('Profile updated'); onSaved(); } catch (error) { setMessage(error.response?.data?.detail || 'Unable to update profile'); } };
  const markRead = async (id) => { await axios.patch(`/api/notifications/${id}/read`); setNotifications(notifications.filter((item) => item.id !== id)); };
  return <section className="employee-tools panel"><Notification notifications={notifications} onRead={markRead} /><div className="panel-heading"><h2>My actions</h2><span className="live-status">{message}</span></div><div className="employee-action-grid"><div><h3>Today's attendance</h3><button className="primary-button" onClick={openRecord ? checkOut : checkIn}>{openRecord ? 'Check out' : 'Check in'} <span>-&gt;</span></button></div><form onSubmit={applyLeave}><h3>Apply for leave</h3><div className="date-pair"><input type="date" value={leave.start_date} onChange={(event) => setLeave({ ...leave, start_date: event.target.value })} /><input type="date" value={leave.end_date} onChange={(event) => setLeave({ ...leave, end_date: event.target.value })} /></div><input value={leave.leave_type} onChange={(event) => setLeave({ ...leave, leave_type: event.target.value })} placeholder="Paid, sick, or unpaid" /><input value={leave.remarks} onChange={(event) => setLeave({ ...leave, remarks: event.target.value })} placeholder="Remarks" /><button className="primary-button">Submit leave <span>-&gt;</span></button></form><form onSubmit={updateProfile}><h3>Edit profile</h3><input value={profile.phone} onChange={(event) => setProfile({ ...profile, phone: event.target.value })} placeholder="Phone number" /><input value={profile.address} onChange={(event) => setProfile({ ...profile, address: event.target.value })} placeholder="Address" /><input value={profile.profile_picture} onChange={(event) => setProfile({ ...profile, profile_picture: event.target.value })} placeholder="Profile picture URL" /><button className="primary-button">Save profile <span>-&gt;</span></button></form></div></section>;
}
