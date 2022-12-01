// display school name input box only if school is selected
document.querySelector("#selection").addEventListener("click", (e) => {
    console.log(e.target.id)
    if (e.target.id == "school") {
        if (document.querySelector("#school").checked) {
            document.querySelector("#dispSchoolName").classList.remove("hide")
        }
    } else if (e.target.id == "provider") {
        document.querySelector("#dispSchoolName").classList.add("hide")
    }
})

// validation
document.querySelector("#submit").addEventListener("click", (e) => {

    if (document.querySelector("#school").checked) {
        if (document.querySelector("#schoolName").value.trim() == "") {
            document.querySelector("#schoolNameError").innerText = "School name cannot be blank."
            e.preventDefault()
        }
    }
    if (document.querySelector("#email").value.trim() == "") {
        document.querySelector("#emailError").innerText = "Email cannot be blank."
        e.preventDefault()
    }

})