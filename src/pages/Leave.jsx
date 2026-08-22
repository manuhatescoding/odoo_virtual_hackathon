import LeaveTable from '../components/LeaveTable';
export default function Leave({ requests = [] }) { return <section><h1>Leave</h1><LeaveTable requests={requests} /></section>; }
