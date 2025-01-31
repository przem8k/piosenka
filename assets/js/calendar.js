const CALENDAR_ID = "783da56c0eb669182662debbda9deac997e1348cd94ad6e42ff6f697854b9e8a@group.calendar.google.com";
const MAX_EVENTS = 10;

async function fetchEvents() {
    const url = `https://www.googleapis.com/calendar/v3/calendars/${CALENDAR_ID}/events?key=${CALENDAR_API_KEY}&maxResults=${MAX_EVENTS}&orderBy=startTime&singleEvents=true`;

    try {
        const eventsList = document.getElementById("pzt-upcoming-events");
        if (!eventsList) {
            return;
        }

        const response = await fetch(url);
        const data = await response.json();
        eventsList.innerHTML = ""; // Clear loading text

        if (data.items) {
            data.items.forEach(event => {
                const li = document.createElement("li");

                const eventTitle = event.summary || "Wydarzenie";
                const eventDate = event.start.dateTime || event.start.date;
                const eventLink = event.htmlLink;

                const eventDateFormatted = new Date(eventDate).toLocaleDateString('en-GB').replace(/\//g, '.');
                const eventLocation = event.location || "";
                li.innerHTML = `<span class="glyphicon glyphicon-calendar"></span> ${eventDateFormatted}, <b>${eventLocation}</b> <a href="${eventLink}" target="_blank">${eventTitle}</a>`;
                eventsList.appendChild(li);
            });
        } else {
            eventsList.innerHTML = "<li>Brak nadchodzących wydarzeń.</li>";
        }
    } catch (error) {
        console.error("Error fetching events:", error);
        document.getElementById("pzt-upcoming-events").innerHTML = "<li>Wystąpił błąd.</li>";
    }
}

fetchEvents();