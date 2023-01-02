if (document.querySelector("#providerEditForm") || document.querySelector("#schoolEditForm")) {

}
function validation(e) {
    // remove all errors
    e.preventDefault()
    removeErrors()
    // Check that the name is not empty
    if (document.querySelector("#name").value.trim() == "") {
        document.querySelector("#nameError").innerText = "Name cannot be blank."
        e.preventDefault()
        return true
    } else {
        // have to set it back to enabled otherwise wtforms will not get this field's data
        if (document.querySelector("#providerEditForm") || document.querySelector("#providerEditForm")) {

        }
        document.querySelector("#province_id").disabled = false
        if (document.querySelector("#dishEditForm") || document.querySelector("#dishAddForm")) {
            document.querySelector("#guidelines").disabled = false
        }

    }

    // if address is empty, remove the geocodes
    if (document.querySelector("#address").value.trim() == "") {
        document.querySelector("#geolat").value = null
        document.querySelector("#geolong").value = null
    }

}

function removeErrors() {
    document.querySelector("#nameError").innerText = ""
}