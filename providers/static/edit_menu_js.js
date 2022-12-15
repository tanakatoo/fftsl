// set minimum date to be today
function setMinDate() {
    let today = new Date()
    let dd = today.getDate()
    let mm = today.getMonth() + 1 //January is 0!
    const yyyy = today.getFullYear();

    if (dd < 10) {
        dd = '0' + dd;
    }

    if (mm < 10) {
        mm = '0' + mm;
    }

    today = yyyy + '-' + mm + '-' + dd;
    document.querySelector("#date").setAttribute("min", today);
    document.querySelector("#startDate").setAttribute("min", today);
    document.querySelector("#endDate").setAttribute("min", today);
}

// set event listeners on the dates so they can delete them
function addEventListenerOnDates() {
    datesTable = document.querySelector("#datesTable")
    datesTD = datesTable.getElementsByTagName("td")
    datesTD = Array.from(datesTD)
    // if the id is not empty, it is a delete button
    datesTD.forEach(td => {
        if (td.id != "") {
            td.addEventListener("click", (e) => deleteDay(e))
        }
    })
}

// add the already saved dates so that we can add it agan
function addDateToHidden() {

}


// Get recurring dates
document.querySelector("#addRecurringDate").addEventListener("click", (e) => {

    e.preventDefault()
    // see which radio button is selected and get the name of day

    if (document.querySelector("#startDate").value != "" && document.querySelector("#endDate").value != 0 && document.querySelector('input[name="days"]:checked')) {
        let selectedDayName = document.querySelector('input[name="days"]:checked').labels[0].innerText
        let selectedDayId = document.querySelector('input[name="days"]:checked').value
        document.querySelector("#recurringDateError").innerText = ""

        let id = 'd' + selectedDayId + document.querySelector("#startDate").value.replaceAll('-', '') + document.querySelector("#endDate").value.replaceAll('-', '') //id needs a character


        // if id is not already selected, add it
        if (!document.querySelector(`#${id}`)) {
            datesTbody = document.querySelector("#recurringDayTable")
            const row = document.createElement("tr");
            const cell = document.createElement("td");
            const cellText = document.createTextNode("Every " + selectedDayName + " from " + document.querySelector("#startDate").value + " - " + document.querySelector("#endDate").value);

            const cellDel = document.createElement("td")
            const cellTextDel = document.createTextNode("X");

            cellDel.id = id
            cell.appendChild(cellText)
            cellDel.appendChild(cellTextDel)

            row.appendChild(cell)
            row.appendChild(cellDel)
            datesTbody.appendChild(row)

            //make X clickable to delete
            document.querySelector(`#${id}`).addEventListener("click", (e) => deleteDay(e))

            //add date to hidden input to be saved in db
            if (document.querySelector("#recurring_dates").value != '') {
                document.querySelector("#recurring_dates").value += ','
            }
            //remove the d, 2nd number is the day, next 8 is start date and 8 after that is end date
            document.querySelector("#recurring_dates").value += selectedDayId + ":" + document.querySelector("#startDate").value + ":" + document.querySelector("#endDate").value //id needs a character


        } else {
            document.querySelector("#recurringDateError").innerText = "Date already added"
        }

    } else {
        document.querySelector("#recurringDateError").innerText = "Select both start and end dates and day of the week. If you wish to select specific dates, set it below."
    }

})

// Get dates available
document.querySelector("#addDate").addEventListener("click", (e) => {

    e.preventDefault()
    if (document.querySelector("#date").value != "" && !document.querySelector(`#${'d' + document.querySelector("#date").value.replaceAll('-', '')}`)) {
        document.querySelector("#dateError").innerText = ""
        datesTbody = document.querySelector("#datesTable")
        const row = document.createElement("tr");
        const cell = document.createElement("td");
        const cellText = document.createTextNode(document.querySelector("#date").value);

        const cellDel = document.createElement("td")
        const cellTextDel = document.createTextNode("X");

        cellDel.id = 'd' + document.querySelector("#date").value.replaceAll('-', '') //id needs a character

        cell.appendChild(cellText)
        cellDel.appendChild(cellTextDel)
        row.appendChild(cell)
        row.appendChild(cellDel)
        datesTbody.appendChild(row)

        //make X clickable to delete
        document.querySelector(`#d${document.querySelector("#date").value.replaceAll('-', '')}`).addEventListener("click", (e) => deleteDay(e))

        //add date to hidden input to be saved in db
        if (document.querySelector("#dates_avail").value != '') {
            document.querySelector("#dates_avail").value += ','
        }
        document.querySelector("#dates_avail").value += document.querySelector("#date").value


    } else if (document.querySelector(`#${'d' + document.querySelector("#date").value.replaceAll('-', '')}`)) {
        document.querySelector("#dateError").innerText = "Date already added"
    } else {
        document.querySelector("#dateError").innerText = "Select date"
    }

})

document.querySelector("#datesTable").addEventListener("click", (e) => {
    e.preventDefault()
    // see which dates are deleted
    console.log(e.target)
})

function deleteDay(e) {
    e.target.parentElement.remove()
}

setMinDate()
addEventListenerOnDates()