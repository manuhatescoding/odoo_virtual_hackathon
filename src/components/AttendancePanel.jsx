import { useState } from 'react';
import axios from 'axios';
import './workspace-panels.css';

const dateLabel = (value) => value ? new Date(value).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }) : '-';

export default function AttendancePanel({ records = [], admin, onSaved }) {
  const [message, setMessage] = useState('');
  const openRecords = records.filter((record) => !record.check_out);
  const checkout = async (id) => {
    try { await axios.patch(`/api/attendance/${id}/checkout`); setMessage('Attendance record closed'); onSaved(); }
    catch (error) { setMessage(error.response?.data?.detail || 'Could not close attendance record'); }
  };
  return <section className="panel full-panel"><div className="panel-heading"><div><h2>{admin ? 'All attendance records' : 'My attendance records'}</h2><p className="muted">{openRecords.length} open record{openRecords.length === 1 ? '' : 's'} need checkout.</p></div>{message && <span className="live-status">{message}</span>}</div>{openRecords.length > 0 && <div className="open-attendance"><strong>Open attendance records</strong><div>{openRecords.map((record) => <button key={record.id} onClick={() => checkout(record.id)} title="Check out this attendance record">&#9209; Employee #{record.employee_id} - Check out</button>)}</div></div>}<div className="table-scroll"><table><thead><tr><th>Employee</th><th>Date</th><th>Check in</th><th>Check out</th><th>Status</th></tr></thead><tbody>{records.map((item) => <tr key={item.id}><td>#{item.employee_id}</td><td>{dateLabel(item.date)}</td><td>{new Date(item.check_in).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</td><td>{item.check_out ? new Date(item.check_out).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) : 'Open'}</td><td>{item.status}</td></tr>)}</tbody></table></div></section>;
}
