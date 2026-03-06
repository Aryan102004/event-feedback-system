document.addEventListener("DOMContentLoaded", function () {

    const addEventBtn = document.getElementById("addEventBtn");
    const eventFormContainer = document.getElementById("eventFormContainer");
    const saveEventBtn = document.getElementById("saveEventBtn");
    const eventsGrid = document.getElementById("eventsGrid");

    addEventBtn.addEventListener("click", function () {
        eventFormContainer.classList.toggle("hidden");
    });

    saveEventBtn.addEventListener("click", function () {

        const title = document.getElementById("eventTitle").value.trim();
        const date = document.getElementById("eventDate").value;
        const description = document.getElementById("eventDescription").value.trim();

        if (!title || !date || !description) {
            alert("Please fill all fields");
            return;
        }

        const eventCard = document.createElement("div");
        eventCard.classList.add("event-card");

        eventCard.innerHTML = `
            <h3>${title}</h3>
            <p>Date: ${date}</p>
            <p>${description}</p>
        `;

        eventsGrid.appendChild(eventCard);

        document.getElementById("eventTitle").value = "";
        document.getElementById("eventDate").value = "";
        document.getElementById("eventDescription").value = "";

        eventFormContainer.classList.add("hidden");
    });

});