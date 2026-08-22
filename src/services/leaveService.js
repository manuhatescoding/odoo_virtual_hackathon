import axios from 'axios';
export const getLeaves = () => axios.get('/api/leave');
export const createLeave = (request) => axios.post('/api/leave', request);
export default { getLeaves, createLeave };
