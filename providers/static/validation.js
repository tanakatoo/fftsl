// all forms have the submit button, and we need validation for all the forms
document.querySelector("#submit").addEventListener("click", validation)

function validation(e) {
    // remove all errors

    removeErrors()
    // for provider edit info and school edit info forms
    if (document.querySelector("#providerEditForm") || document.querySelector("#schoolEditForm")) {
        // Check that the name is not empty
        if (document.querySelector("#name").value.trim() == "") {
            document.querySelector("#nameError").innerText = "Name cannot be blank."
            e.preventDefault()
            return true
        }
        else {
            // have to set it back to enabled otherwise wtforms will not get this field's data
            document.querySelector("#province_id").disabled = false
        }

        // if address is empty, remove the geocodes
        if (document.querySelector("#address").value.trim() == "") {
            document.querySelector("#geolat").value = null
            document.querySelector("#geolong").value = null
        }

    }

    // for dish edit and dish add forms
    if (document.querySelector("#dishEditForm") || document.querySelector("#dishAddForm")) {
        if (document.querySelector("#name").value.trim() == "") {
            document.querySelector("#nameError").innerText = "Name cannot be blank."
            e.preventDefault()
            return true
        }
        else {
            // set it back to enabled otherwise wtforms will not get this field's data
            document.querySelector("#guidelines").disabled = false
        }
    }
}

function removeErrors() {
    document.querySelector("#nameError").innerText = ""
}