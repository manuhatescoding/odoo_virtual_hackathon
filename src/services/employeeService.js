import axios from 'axios';
export const getEmployees = () => axios.get('/api/employees');
export const createEmployee = (employee) => axios.post('/api/employees', employee);
export const updateEmployee = (id, employee) => axios.put(`/api/employees/${id}`, employee);
export const deleteEmployee = (id) => axios.delete(`/api/employees/${id}`);
export default { getEmployees, createEmployee, updateEmployee, deleteEmployee };
