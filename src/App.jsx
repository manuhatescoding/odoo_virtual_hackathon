import React, { useEffect, useState } from 'react';
import axios from 'axios';
import AdminTools from './components/AdminTools';
import EmployeeTools from './components/EmployeeTools';
import Notification from './components/Notification';
import AuthScreen from './components/AuthScreen';
import HelpCentre from './components/HelpCentre';
import AttendancePanel from './components/AttendancePanel';
import ReportsPanel from './components/ReportsPanel';
import ProfilePanel from './components/ProfilePanel';
import './styles.css';
import './role-login.css';

const empty = { employees: [], attendance: [], leaves: [], payroll: [], notifications: [] };
const interval = Number(import.meta.env.VITE_REFRESH_INTERVAL_MS || 10000);
const dateLabel = (value) => value ? new Date(value).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }) : '-';
const money = (value) => new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 }).format(value || 0);

function App() {
  const [user, setUser] = useState(() => {
    const token = localStorage.getItem('dayflow_token');
    if (token) axios.defaults.headers.common.Authorization = `Bearer ${token}`;
    return token ? JSON.parse(localStorage.getItem('dayflow_user') || 'null') : null;
  });
  const [section, setSection] = useState('Overview');
  const [data, setData] = useState(empty);
  const [toast, setToast] = useState('');
  const loadData = async () => {
    try {
      const results = await Promise.all(['/api/employees', '/api/attendance', '/api/leave', '/api/payroll', '/api/notifications'].map((url) => axios.get(url)));
      setData({ employees: results[0].data, attendance: results[1].data, leaves: results[2].data, payroll: results[3].data, notifications: results[4].data });
    } catch (error) {
      setToast(error.response?.status === 401 ? 'Session expired. Please sign in again.' : 'API connection unavailable');
    }
  };
  useEffect(() => { if (!user) return undefined; loadData(); const timer = setInterval(loadData, interval); return () => clearInterval(timer); }, [user]);
  useEffect(() => { if (!toast) return undefined; const timer = setTimeout(() => setToast(''), 3000); return () => clearTimeout(timer); }, [toast]);
  if (!user) return <AuthScreen onLogin={setUser} />;
  const today = new Date().toISOString().slice(0, 10);
  const present = data.attendance.filter((item) => item.date === today).length;
  const payrollTotal = data.payroll.reduce((sum, item) => sum + Number(item.net_salary ?? item.salary ?? 0), 0);
  const nav = user.role === 'admin' ? ['Overview', 'People', 'Profile', 'Attendance', 'Leave', 'Payroll', 'Reports', 'Help'] : ['Overview', 'Profile', 'Attendance', 'Leave', 'Payroll', 'Help'];
  const markNotificationRead = async (id) => { await axios.patch(`/api/notifications/${id}/read`); loadData(); };
  const logout = () => { localStorage.removeItem('dayflow_user'); localStorage.removeItem('dayflow_token'); delete axios.defaults.headers.common.Authorization; setUser(null); };
  return <div className="app-shell">
    <aside className="sidebar"><div className="sidebar-brand"><span className="brand-mark small">D</span><span>dayflow</span></div><div className="workspace-label">{user.role === 'admin' ? 'HR WORKSPACE' : 'MY WORKSPACE'}</div><nav>{nav.map((item, index) => <button key={item} className={section === item ? 'nav-item active' : 'nav-item'} onClick={() => setSection(item)}><span className="nav-number">0{index + 1}</span>{item}</button>)}</nav><div className="sidebar-bottom"><button className="logout" onClick={logout}>Sign out</button></div></aside>
    <main className="main-content"><header className="topbar"><div className="breadcrumb">Workspace <span>/</span> {section}</div><Notification notifications={data.notifications} onRead={markNotificationRead} /><div className="user-chip"><div className="avatar">{user.full_name?.slice(0, 2).toUpperCase()}</div><span>{user.full_name}</span><small>{user.role}</small></div></header>
      <div className="content-wrap"><section className="page-heading"><div><p className="eyebrow">DAYFLOW / PEOPLE OPERATIONS</p><h1>{section === 'Overview' ? <>Good morning, <em>{user.full_name.split(' ')[0]}.</em></> : <em>{section}</em>}</h1><p className="muted">Live people operations for your workspace.</p></div><div className="heading-actions"><span className="live-status"><span className="pulse-dot" /> Live sync on</span><button className="secondary-button" onClick={loadData}>Refresh</button></div></section>
        {section === 'Overview' && <><Overview data={data} present={present} payrollTotal={payrollTotal} onPeople={() => setSection(user.role === 'admin' ? 'People' : 'Profile')} />{user.role === 'employee' && <EmployeeTools employee={data.employees[0]} attendance={data.attendance} onSaved={loadData} />}</>}
        {section === 'People' && user.role === 'admin' && <><AdminTools employees={data.employees} attendance={data.attendance} onSaved={loadData} onAttendance={() => setSection('Attendance')} /><Panel title="People directory"><Table headers={['Name', 'Job title', 'Department', 'Joining date']} rows={data.employees.map((item) => [item.name, item.job_title, item.department, dateLabel(item.joining_date)])} /></Panel></>}
        {section === 'Profile' && <ProfilePanel user={user} />}
        {section === 'Attendance' && <AttendancePanel records={data.attendance} admin={user.role === 'admin'} onSaved={loadData} />}
        {section === 'Leave' && <LeavePanel leaves={data.leaves} admin={user.role === 'admin'} onSaved={loadData} />}
        {section === 'Payroll' && <Panel title={user.role === 'admin' ? 'Employee payroll' : 'My payroll'}><Table headers={['Employee', 'Effective date', 'Basic salary', 'Allowances', 'Net salary']} rows={data.payroll.map((item) => [`#${item.employee_id}`, dateLabel(item.effective_date), money(item.basic_salary ?? item.salary), money(item.allowances), money(item.net_salary ?? item.salary)])} /></Panel>}
        {section === 'Reports' && user.role === 'admin' && <ReportsPanel />}
        {section === 'Help' && <HelpCentre />}
      </div>
    </main>{toast && <div className="toast">{toast}</div>}
  </div>;
}

function LeavePanel({ leaves, admin, onSaved }) { return <Panel title={admin ? 'All leave requests' : 'My leave requests'}><div className="table-scroll"><table><thead><tr><th>Employee</th><th>Leave type</th><th>Dates</th><th>Status</th>{admin && <th>Actions</th>}</tr></thead><tbody>{leaves.map((item) => <tr key={item.id}><td>#{item.employee_id}</td><td>{item.leave_type}</td><td>{dateLabel(item.start_date)} - {dateLabel(item.end_date)}</td><td>{item.status}</td>{admin && <td className="row-actions"><button onClick={() => updateLeave(item.id, 'Approved', onSaved)}>Approve</button><button onClick={() => updateLeave(item.id, 'Rejected', onSaved)}>Reject</button></td>}</tr>)}</tbody></table></div></Panel>; }
async function updateLeave(id, status, onSaved) { await axios.patch(`/api/leave/${id}/status?status=${status}`); onSaved(); }
function Overview({ data, present, payrollTotal, onPeople }) { return <><section className="metrics-grid"><Metric label="Team members" value={data.employees.length} change="Active directory" accent="blue" /><Metric label="Present today" value={present} change="Live attendance" accent="green" /><Metric label="Pending leave" value={data.leaves.filter((item) => item.status === 'Pending').length} change="Needs attention" accent="yellow" /><Metric label="Net payroll" value={money(payrollTotal)} change={`${data.payroll.length} records`} accent="coral" /></section><section className="panel directory-panel"><div className="panel-heading"><h2>People directory</h2><button onClick={onPeople}>Manage people -&gt;</button></div><Table headers={['Name', 'Job title', 'Department', 'Joining date']} rows={data.employees.slice(0, 5).map((item) => [item.name, item.job_title, item.department, dateLabel(item.joining_date)])} /></section></>; }
function Metric({ label, value, change, accent }) { return <div className={`metric ${accent}`}><span>{label}</span><strong>{value}</strong><small>{change}</small></div>; }
function Panel({ title, children }) { return <section className="panel full-panel"><div className="panel-heading"><h2>{title}</h2></div>{children}</section>; }
function Table({ headers, rows }) { return rows.length ? <div className="table-scroll"><table><thead><tr>{headers.map((header) => <th key={header}>{header}</th>)}</tr></thead><tbody>{rows.map((row, index) => <tr key={index}>{row.map((cell, cellIndex) => <td key={cellIndex}>{cell}</td>)}</tr>)}</tbody></table></div> : <div className="empty">Nothing to show yet</div>; }

export default App;
