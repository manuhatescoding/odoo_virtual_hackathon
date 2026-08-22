import axios from 'axios';
export const getAttendance = () => axios.get('/api/attendance');
export const createAttendance = (record) => axios.post('/api/attendance', record);
export default { getAttendance, createAttendance };
