import { useMemo, useState } from 'react';
import './help-centre.css';

const faqs = [
  ['Getting started', 'How do I request leave?', 'Open Leave, choose the dates and leave type, add a note if needed, and submit. HR decisions appear in your notifications.'],
  ['Payroll', 'Where can I find my payslips?', 'Open Payroll to see published salary, allowances, deductions, net salary, and effective dates.'],
  ['Profile', 'How do I update my profile?', 'Open Profile, select Edit profile, update your contact details, and save.'],
  ['Attendance', 'How do I close an open attendance record?', 'Open Attendance and select Check out beside the open record. HR can close open records for the team.'],
  ['Notifications', 'Why did I receive a notification?', 'Dayflow sends alerts when leave requests change status, payroll is published, or a leave request is submitted.'],
  ['Troubleshooting', 'Why is my data not loading?', 'Check that the backend is running on port 8000, then select Refresh. A fresh login restores your session if it expired.'],
];

export default function HelpCentre() {
  const [query, setQuery] = useState('');
  const filtered = useMemo(() => faqs.filter(([, question, answer]) => `${question} ${answer}`.toLowerCase().includes(query.toLowerCase())), [query]);
  return <section className="help-centre"><div className="help-hero"><div><p className="eyebrow">SUPPORT DESK</p><h2>How can we help?</h2><p className="muted">Find answers for the everyday work inside Dayflow.</p></div><span className="help-hero-icon" aria-hidden="true">&#10067;</span></div><div className="help-tools"><label htmlFor="help-search">Search help<input id="help-search" value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Search leave, payroll, profile..." /></label><div className="help-shortcuts"><span>&#128197; Attendance</span><span>&#128176; Payroll</span><span>&#128100; Profile</span></div></div><div className="faq-list">{filtered.length ? filtered.map(([category, question, answer]) => <details key={question}><summary><span className="faq-category">{category}</span>{question}</summary><p className="muted">{answer}</p></details>) : <p className="empty">No help articles match your search.</p>}</div><div className="support-note"><strong>Still need help?</strong><span>Contact your HR administrator with the screen name and action that failed.</span></div></section>;
}
