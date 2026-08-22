import { useState } from 'react';
import './notification.css';

export default function Notification({ notifications = [], onRead }) {
	const [open, setOpen] = useState(false);
	const unread = notifications.filter((item) => !item.is_read);
	return <div className="notification-center"><button className="notification-button" title="Notifications" aria-label="Notifications" aria-expanded={open} onClick={() => setOpen(!open)}><span aria-hidden="true">&#128276;</span>{unread.length > 0 && <span className="notification-count">{unread.length}</span>}</button>{open && <div className="notification-menu"><div className="notification-menu-heading"><strong>Notifications</strong><button onClick={() => setOpen(false)} aria-label="Close notifications">&#10005;</button></div>{notifications.length ? notifications.slice(0, 8).map((item) => <button className={item.is_read ? 'notification-item read' : 'notification-item'} key={item.id} onClick={() => onRead?.(item.id)}><strong>{item.title}</strong><small>{item.message}</small></button>) : <p className="notification-empty">You are all caught up.</p>}</div>}</div>;
}
