
document.querySelector("#reviewBtn").addEventListener('click', (e) => {
    validation(e)
    // remove errors specific for this form
    document.querySelector("#inspectionFileError").innerText = ""
    if (!document.querySelector("#inspectionFile").value) {
        e.preventDefault()
        document.querySelector("#inspectionFileError").innerText = "Required for review"
    }
    // ok to submit for inspection
    document.querySelector("#submit_inspection").value = 'True'

})