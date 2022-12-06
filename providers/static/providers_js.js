const MAPQUEST_SEARCH_API = 'http://www.mapquestapi.com/search/v3/prediction'

document.querySelector("#address").addEventListener("input", getAddresses)
let timer

function getAddresses() {
    input = document.querySelector("#address").value
    if (input.length > 2) {

        if (timer) {
            clearTimeout(timer)
        }
        // we are limited to Ontario, Canada right now, so search only those
        try {
            timer = setTimeout(async function () {
                // call axios to get info from db
                const res = await axios({
                    url: `${MAPQUEST_SEARCH_API}`,
                    method: "GET",
                    params: {
                        key: 'F9Y0WPSgu8hi7cjUdvVIfhrHmLXjM7sx',
                        limit: 5,
                        collection: 'address',
                        countryCode: 'CA',
                        q: input
                    }
                })

                // put all address information in an array of objects
                showAddresses = makeAddressObject(res)
                // make a table under the input box for the results
                table = makeAutoCompleteTable(showAddresses)
                // add click event on table and remove table once selected
                selectAddress(table, showAddresses)


            }, 1500)
        } catch (e) {
            console.log('error in getting string')
        }

    }

}

function makeAddressObject(res) {
    let showAddresses = []
    let j = 0
    getAddresses.length = 0

    for (let i = 0; i < res.data.results.length; i++) {

        // only take results in Ontario for now
        if (res.data.results[i].place.properties.state == "Ontario") {
            showAddresses[j] = {
                fullAddress: res.data.results[i].displayString,
                street: res.data.results[i].place.properties.street,
                province: res.data.results[i].place.properties.state,
                city: res.data.results[i].place.properties.city,
                lat: res.data.results[i].place.geometry.coordinates[1],
                long: res.data.results[i].place.geometry.coordinates[0]
            }
            j++
        }
    }
    console.log(res.data.results)

    return showAddresses
}

function makeAutoCompleteTable(showAddresses) {

    let tableDiv = document.querySelector(".autoAddress")
    let table = document.createElement('table')
    let tblBody = document.createElement('tbody')

    // create one cell for each address line
    for (let i = 0; i < showAddresses.length; i++) {
        // creates a table row
        const row = document.createElement("tr");
        const cell = document.createElement("td");
        const cellText = document.createTextNode(showAddresses[i].fullAddress);
        cell.dataset.id = i
        cell.appendChild(cellText);
        row.appendChild(cell);

        tblBody.appendChild(row);
    }
    table.appendChild(tblBody)
    tableDiv.appendChild(table)
    return table
}

function selectAddress(table) {
    table.addEventListener('click', function (e) {
        // fill address input with selected address
        let id = e.target.dataset.id
        table.remove()
        // remove hidden value and any new values that were added to the city select option
        if (document.querySelector("#newCity")) {
            //remove the optino from the list
            console.log('dataset id for ihiden is ' + document.querySelector("#newCity").dataset.id)
            document.querySelector("#city_id").remove(parseInt(document.querySelector("#newCity").dataset.id))
            document.querySelector("#newCity").remove() //remove the hidden tag to add to the db

        }
        completeAddress(id, showAddresses)
    })
}

function completeAddress(id, showAddresses) {
    document.querySelector("#address").value = showAddresses[id].street
    citySelect = document.querySelector("#city_id")
    let selected = false
    // select starts at id 1, not 0
    for (let i = 0; i < citySelect.options.length; i++) {

        if (citySelect.options[i].text == showAddresses[id].city) {
            citySelect.selectedIndex = i
            selected = true
            break
        }
    }
    if (!selected) {
        // means not in db, have to add it
        let newOption = new Option(showAddresses[id].city, citySelect.options.length + 1)
        citySelect.add(newOption)
        citySelect.selectedIndex = citySelect.options.length - 1

        // add it as a hidden element to be passed to the server to add to the db
        hidden = document.createElement('input')
        hidden.setAttribute("type", "hidden")
        hidden.id = "newCity"
        hidden.name = "newCity"
        hidden.dataset.id = citySelect.selectedIndex // this is to be able to select this option to delete it from the select dropdown if required
        hidden.value = citySelect.options[citySelect.selectedIndex].text
        document.querySelector("#providerEditForm").append(hidden)

    }
    // do the same for province if this is used outside Ontario

    // add lat and long coordinates to hidden to pass to db
    document.querySelector("#geolat").value = showAddresses[id].lat
    document.querySelector("#geolong").value = showAddresses[id].long
}