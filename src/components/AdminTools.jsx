import { useState } from 'react';
import axios from 'axios';

const today = new Date().toISOString().slice(0, 10);

export default function AdminTools({ employees, attendance, onSaved, onAttendance }) {
  const [employee, setEmployee] = useState({ name: '', job_title: 'Employee', department: 'General', phone: '' });
  const [leave, setLeave] = useState({ employee_id: employees[0]?.id || '', leave_type: 'Annual', start_date: today, end_date: today, remarks: '' });
  const [payroll, setPayroll] = useState({ employee_id: employees[0]?.id || '', basic_salary: '', allowances: '0', deductions: '0', effective_date: today });
  const [message, setMessage] = useState('');
  const submit = async (event, url, payload, reset) => {
    event.preventDefault();
    try { await axios.post(url, payload); setMessage('Saved successfully'); reset(); onSaved(); }
    catch (error) { setMessage(error.response?.data?.detail || 'Could not save record'); }
  };
  const employeeOptions = employees.map((item) => <option value={item.id} key={item.id}>{item.name}</option>);
  const openRecords = attendance.filter((item) => !item.check_out);
  const checkout = async (id) => {
    try { await axios.patch(`/api/attendance/${id}/checkout`); setMessage('Attendance record closed'); onSaved(); }
    catch (error) { setMessage(error.response?.data?.detail || 'Could not close attendance record'); }
  };
  return <section className="admin-tools panel">
    <div className="panel-heading"><h2>Manage workspace</h2><span className="live-status">{message}</span></div>
    <div className="tool-grid">
      <form onSubmit={(event) => submit(event, '/api/employees', employee, () => setEmployee({ name: '', job_title: 'Employee', department: 'General', phone: '' }))}><h3>Add employee</h3><input required placeholder="Full name" value={employee.name} onChange={(event) => setEmployee({ ...employee, name: event.target.value })} /><input placeholder="Job title" value={employee.job_title} onChange={(event) => setEmployee({ ...employee, job_title: event.target.value })} /><input placeholder="Department" value={employee.department} onChange={(event) => setEmployee({ ...employee, department: event.target.value })} /><input placeholder="Phone" value={employee.phone} onChange={(event) => setEmployee({ ...employee, phone: event.target.value })} /><button className="primary-button">Create employee</button></form>
      <form onSubmit={(event) => submit(event, '/api/leave', { ...leave, employee_id: Number(leave.employee_id) }, () => setLeave({ ...leave, remarks: '' }))}><h3>Request leave</h3><select value={leave.employee_id} onChange={(event) => setLeave({ ...leave, employee_id: event.target.value })}>{employeeOptions}</select><input placeholder="Leave type" value={leave.leave_type} onChange={(event) => setLeave({ ...leave, leave_type: event.target.value })} /><div className="date-pair"><input type="date" value={leave.start_date} onChange={(event) => setLeave({ ...leave, start_date: event.target.value })} /><input type="date" value={leave.end_date} onChange={(event) => setLeave({ ...leave, end_date: event.target.value })} /></div><input placeholder="Remarks" value={leave.remarks} onChange={(event) => setLeave({ ...leave, remarks: event.target.value })} /><button className="primary-button">Submit request</button></form>
      <form onSubmit={(event) => submit(event, '/api/payroll', { ...payroll, employee_id: Number(payroll.employee_id), basic_salary: Number(payroll.basic_salary), allowances: Number(payroll.allowances), deductions: Number(payroll.deductions) }, () => setPayroll({ ...payroll, basic_salary: '' }))}><h3>Add payroll</h3><select value={payroll.employee_id} onChange={(event) => setPayroll({ ...payroll, employee_id: event.target.value })}>{employeeOptions}</select><input required type="number" min="1" placeholder="Basic salary" value={payroll.basic_salary} onChange={(event) => setPayroll({ ...payroll, basic_salary: event.target.value })} /><input type="number" min="0" placeholder="Allowances" value={payroll.allowances} onChange={(event) => setPayroll({ ...payroll, allowances: event.target.value })} /><input type="number" min="0" placeholder="Deductions" value={payroll.deductions} onChange={(event) => setPayroll({ ...payroll, deductions: event.target.value })} /><button className="primary-button">Save payroll</button></form>
    </div>
    <div className="checkout-row"><button className="attendance-link" onClick={onAttendance}>&#9209; Open attendance records ({openRecords.length})</button>{openRecords.slice(0, 3).map((item) => <button key={item.id} onClick={() => checkout(item.id)}>Employee #{item.employee_id} check out</button>)}</div>
  </section>;
}
