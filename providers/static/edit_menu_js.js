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
}



// Get dates available
document.querySelector("#addDate").addEventListener("click", (e) => {

    e.preventDefault()
    if (document.querySelector("#date").value != "") {
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
        document.querySelector(`#d${document.querySelector("#date").value.replaceAll('-', '')}`).addEventListener("click", (e) => {
            // delete whole row
            e.target.parentElement.remove()
        })

        //add date to hidden input to be saved in db
        if (document.querySelector("#dates_avail").value != '') {
            document.querySelector("#dates_avail").value += ','
        }
        document.querySelector("#dates_avail").value += document.querySelector("#date").value


    } else {
        document.querySelector("#dateError").innerText = "Select date"
    }

})

document.querySelector("#datesTable").addEventListener("click", (e) => {
    e.preventDefault()
    // see which dates are deleted
    console.log(e.target)
})

setMinDate()