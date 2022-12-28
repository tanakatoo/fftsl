document.querySelector("#reviewBtn").addEventListener('click', (e) => {
    if (!document.querySelector("#inspectionFile").value) {
        e.preventDefault()
        document.querySelector("#inspectionFileError").innerText = "Required for submission"
    }


})