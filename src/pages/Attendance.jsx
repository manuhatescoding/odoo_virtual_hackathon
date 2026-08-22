import AttendanceTable from '../components/AttendanceTable';
export default function Attendance({ records = [] }) { return <section><h1>Attendance</h1><AttendanceTable records={records} /></section>; }
