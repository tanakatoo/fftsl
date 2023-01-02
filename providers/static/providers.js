if (document.querySelector("#providerEditForm")) {
    // if submitted for review already, change button so it is disabled
    if (document.querySelector("#submit_inspection").value == 'True') {
        document.querySelector("#reviewBtn").disabled = true
        document.querySelector("#reviewBtn").innerText = 'Submitted for review'
    }



    document.querySelector("#reviewBtn").addEventListener('click', (e) => {
        validation(e)
        // remove errors specific for this form
        document.querySelector("#inspectionFileError").innerText = ""
        if (!document.querySelector("#inspectionFile").value && !document.querySelector('#submittedFile')) {
            e.preventDefault()
            document.querySelector("#inspectionFileError").innerText = "Required for review"
        }
        // ok to submit for inspection
        document.querySelector("#submit_inspection").value = 'True'

    })


}


