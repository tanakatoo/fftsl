// only run for specific forms
if (document.querySelector("#signupForm")) {
    // user_type-1 = school
    // user_type-0 =provider

    // display school name input box only if school is selected
    document.querySelector("#selection").addEventListener("click", (e) => {
        console.log(e.target.id)
        if (e.target.id == "user_type-1") {
            if (document.querySelector("#user_type-1").checked) {
                document.querySelector("#dispSchoolName").classList.remove("hide")
            }
        } else if (e.target.id == "user_type-0") {
            document.querySelector("#dispSchoolName").classList.add("hide")
        }
    })

    // validation
    document.querySelector("#submit").addEventListener("click", (e) => {

        if (document.querySelector("#user_type-1").checked) {
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
}

if (document.querySelector("#loginForm")) {
    // validation
    document.querySelector("#submit").addEventListener("click", (e) => {

        if (document.querySelector("#email").value.trim() == "") {
            document.querySelector("#emailError").innerText = "Email cannot be blank."
            e.preventDefault()
        }

        if (document.querySelector("#password").value.trim() == "") {
            document.querySelector("#emailError").innerText = "Password cannot be blank."
            e.preventDefault()
        }

        if (document.querySelector("#password").value.trim().length < 9) {
            document.querySelector("#emailError").innerText = "Password must be 8 characters or longer."
            e.preventDefault()
        }
    })
}