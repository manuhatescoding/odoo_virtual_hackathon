import { useEffect, useState } from 'react';
import axios from 'axios';
import './workspace-panels.css';

export default function ReportsPanel() {
  const [reports, setReports] = useState(null);
  const [error, setError] = useState('');
  useEffect(() => { Promise.all(['/api/reports/attendance', '/api/reports/leave', '/api/reports/payroll'].map((url) => axios.get(url))).then(([attendance, leave, payroll]) => setReports({ attendance: attendance.data, leave: leave.data, payroll: payroll.data })).catch(() => setError('Reports are unavailable. Check the API connection and refresh.')); }, []);
  if (error) return <section className="panel full-panel"><h2>HR reports</h2><p className="form-error">{error}</p></section>;
  if (!reports) return <section className="panel full-panel"><h2>HR reports</h2><p className="muted">Loading live reports...</p></section>;
  return <section className="report-grid"><ReportCard icon="&#128197;" title="Attendance" value={reports.attendance.total} detail={Object.entries(reports.attendance.by_status).map(([key, value]) => `${key}: ${value}`).join(' | ') || 'No records yet'} /><ReportCard icon="&#127796;" title="Leave" value={reports.leave.total} detail={Object.entries(reports.leave.by_status).map(([key, value]) => `${key}: ${value}`).join(' | ') || 'No requests yet'} /><ReportCard icon="&#36;" title="Payroll" value={`$${reports.payroll.net_payroll.toLocaleString()}`} detail={`${reports.payroll.total_records} published records`} /></section>;
}
function ReportCard({ icon, title, value, detail }) { return <article className="report-card"><span className="report-icon" aria-hidden="true" dangerouslySetInnerHTML={{ __html: icon }} /><p className="eyebrow">{title}</p><strong>{value}</strong><small>{detail}</small></article>; }
