import axios from 'axios';
export const getPayroll = () => axios.get('/api/payroll');
export const createPayroll = (record) => axios.post('/api/payroll', record);
export default { getPayroll, createPayroll };
