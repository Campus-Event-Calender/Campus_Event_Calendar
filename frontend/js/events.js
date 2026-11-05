let currentEvents = [];

async function loadEvents() {
    const message = document.getElementById('eventMessage');
    try {
        const response = await fetch('/api/events');
        const events = await response.json();
        if (!response.ok) {
            throw new Error(events.error || 'Unable to load events');
        }
        currentEvents = events;
        document.getElementById('eventGrid').innerHTML = events.map(event => `
            <article class="event-card">
                <span class="tag">${escapeHtml(event.category)}</span>
                <h3>${escapeHtml(event.title)}</h3>
                <div class="event-meta">📅 ${formatDate(event.start_time)}<br>
                    📍 ${escapeHtml(event.venue)}<br>
                    👥 ${event.rsvp_count}/${event.capacity} registered</div>
                <div class="event-actions">
                    <button class="button" onclick="showRsvp(${event.id})">RSVP</button>
                    <button class="button secondary" onclick="showEdit(${event.id})">Edit</button>
                    <button class="button danger" onclick="deleteEvent(${event.id})">Delete</button>
                </div>
            </article>`).join('');
        if (message.dataset.persistent !== 'true') {
            message.classList.add('hidden');
            message.textContent = '';
        }
    } catch (error) {
        showEventMessage(error.message || 'Unable to load events', false);
    }
}

function showRsvp(id) {
    const event = currentEvents.find(item => item.id === id);
    if (!event) {
        showEventMessage('This event is no longer available. Refresh the list and try again.', false);
        return;
    }
    document.getElementById('eventModalContent').innerHTML = `
        <span class="tag">${escapeHtml(event.category)}</span><h2>${escapeHtml(event.title)}</h2>
        <p class="muted">${formatDate(event.start_time)} · ${escapeHtml(event.venue)}</p>
        <p>${escapeHtml(event.description)}</p>
        <form onsubmit="submitEventRsvp(event,${event.id})"><div class="form-grid">
            <div class="field"><label>Name</label><input name="student_name" required></div>
            <div class="field"><label>Student ID</label><input name="student_id" required></div>
            <div class="field full"><label>Email</label><input type="email" name="student_email" required></div>
        </div><div class="form-actions"><button class="button">Confirm RSVP</button></div></form>
        <div id="eventRsvpMessage" role="status" aria-live="polite"></div>`;
    document.getElementById('eventModal').classList.remove('hidden');
}

async function submitEventRsvp(ev, id) {
    ev.preventDefault();
    const data = Object.fromEntries(new FormData(ev.target));
    try {
        const response = await fetch(`/api/events/${id}/rsvp`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        });
        const result = await response.json();
        const message = document.getElementById('eventRsvpMessage');
        message.className = `notice ${response.ok ? 'success' : ''}`;
        message.textContent = result.message || result.error || 'Unable to submit RSVP';
        if (response.ok) {
            await loadEvents();
        }
    } catch (error) {
        const message = document.getElementById('eventRsvpMessage');
        message.className = 'notice';
        message.textContent = error.message || 'Unable to submit RSVP';
    }
}

function showCreate() {
    document.getElementById('eventModalContent').innerHTML = `
        <h2>Create Event</h2>${eventFormMarkup({})}`;
    document.getElementById('eventModal').classList.remove('hidden');
}

async function showEdit(id) {
    try {
        const response = await fetch(`/api/events/${id}`);
        const event = await response.json();
        if (!response.ok) {
            throw new Error(event.error || 'Unable to load event');
        }
        document.getElementById('eventModalContent').innerHTML = `
            <h2>Edit Event</h2>${eventFormMarkup(event)}`;
        document.getElementById('eventModal').classList.remove('hidden');
    } catch (error) {
        showEventMessage(error.message || 'Unable to load event', false);
    }
}

function eventFormMarkup(event) {
    const categories = ['Workshop', 'Hackathon', 'Seminar', 'Cultural', 'Sports', 'Other'];
    if (event.category && !categories.includes(event.category)) {
        categories.push(event.category);
    }
    const categoryOptions = categories.map(category =>
        `<option value="${escapeHtml(category)}" ${category === event.category ? 'selected' : ''}>${escapeHtml(category)}</option>`
    ).join('');
    const isEditing = Boolean(event.id);
    return `<form onsubmit="${isEditing ? 'updateEvent' : 'createEvent'}(event${isEditing ? `,${event.id}` : ''})">
        <div class="form-grid">
            <div class="field full"><label>Title</label><input name="title" value="${escapeHtml(event.title || '')}" required></div>
            <div class="field"><label>Category</label><select name="category">${categoryOptions}</select></div>
            <div class="field"><label>Venue</label><input name="venue" value="${escapeHtml(event.venue || 'Campus')}"></div>
            <div class="field"><label>Start</label><input type="datetime-local" name="start_time" value="${dateTimeLocalValue(event.start_time)}" required></div>
            <div class="field"><label>End</label><input type="datetime-local" name="end_time" value="${dateTimeLocalValue(event.end_time)}" required></div>
            <div class="field"><label>Capacity</label><input type="number" name="capacity" value="${event.capacity || 100}" min="1" step="1" required></div>
            <div class="field full"><label>Description</label><textarea name="description">${escapeHtml(event.description || '')}</textarea></div>
        </div>
        <div class="form-actions"><button class="button">${isEditing ? 'Save Changes' : 'Create Event'}</button></div>
        <div id="eventFormMessage" role="status" aria-live="polite"></div>
    </form>`;
}

async function createEvent(ev) {
    ev.preventDefault();
    await submitEventForm(ev, '/api/events', 'POST');
}

async function updateEvent(ev, id) {
    ev.preventDefault();
    await submitEventForm(ev, `/api/events/${id}`, 'PUT');
}

async function submitEventForm(ev, url, method) {
    const data = Object.fromEntries(new FormData(ev.target));
    const start = new Date(data.start_time);
    const end = new Date(data.end_time);
    const message = document.getElementById('eventFormMessage');
    if (Number.isNaN(start.getTime()) || Number.isNaN(end.getTime()) || end <= start) {
        showFormMessage(message, 'End time must be later than start time.', false);
        return;
    }
    if (!/^[0-9]+$/.test(data.capacity) || Number(data.capacity) < 1) {
        showFormMessage(message, 'Capacity must be a positive integer.', false);
        return;
    }
    try {
        const response = await fetch(url, {
            method,
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        });
        const result = await response.json();
        if (!response.ok) {
            showFormMessage(message, result.error || 'Unable to save event', false);
            return;
        }
        closeEventModal();
        await loadEvents();
        showEventMessage(method === 'PUT' ? 'Event updated successfully.' : 'Event created successfully.', true);
    } catch (error) {
        showFormMessage(message, error.message || 'Unable to save event', false);
    }
}

async function deleteEvent(id) {
    if (!window.confirm('Are you sure you want to delete this event? Existing RSVPs and attendance records will also be deleted.')) {
        return;
    }
    try {
        const response = await fetch(`/api/events/${id}`, {method: 'DELETE'});
        const result = await response.json();
        if (!response.ok) {
            throw new Error(result.error || 'Unable to delete event');
        }
        await loadEvents();
        showEventMessage(result.message || 'Event deleted successfully.', true);
    } catch (error) {
        showEventMessage(error.message || 'Unable to delete event', false);
    }
}

function showFormMessage(element, text, success) {
    element.className = `notice ${success ? 'success' : ''}`;
    element.textContent = text;
}

function showEventMessage(text, success) {
    const message = document.getElementById('eventMessage');
    message.textContent = text;
    message.className = `notice ${success ? 'success' : ''}`;
    message.dataset.persistent = 'true';
}

function closeEventModal() {
    document.getElementById('eventModal').classList.add('hidden');
}

function dateTimeLocalValue(value) {
    if (!value) return '';
    const date = new Date(value);
    if (Number.isNaN(date.getTime())) return String(value).slice(0, 16);
    const pad = part => String(part).padStart(2, '0');
    return `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())}T${pad(date.getHours())}:${pad(date.getMinutes())}`;
}

function formatDate(value) {
    return new Date(value).toLocaleString([], {dateStyle: 'medium', timeStyle: 'short'});
}

function escapeHtml(value) {
    return String(value).replace(/[&<>"']/g, character =>
        ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;'}[character])
    );
}

async function loadHomeStats() {
    const response = await fetch('/api/events');
    if (!response.ok) return;
    const events = await response.json();
    const total = events.reduce((sum, event) => sum + event.rsvp_count, 0);
    document.getElementById('homeStats').innerHTML = `
        <div class="stat"><strong>${events.length}</strong><span class="muted">Upcoming events</span></div>
        <div class="stat"><strong>${total}</strong><span class="muted">Confirmed RSVPs</span></div>
        <div class="stat"><strong>${events.reduce((sum, event) => sum + event.capacity, 0)}</strong><span class="muted">Total capacity</span></div>`;
}
