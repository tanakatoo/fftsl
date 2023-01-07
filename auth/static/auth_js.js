// only run for specific forms
if (document.querySelector("#signupForm")) {
    // user_type-2 = provider
    // user_type-1 = school
    // user_type-0 =parent

    // change label for input box
    document.querySelector("#selection").addEventListener("click", (e) => {

        if (e.target.id == "user_type-1") {
            if (document.querySelector("#user_type-1").checked) {
                document.querySelector('label[for="establishment_name"]').textContent = "Name of school"
            }
        } else if (e.target.id == "user_type-0") {
            document.querySelector('label[for="establishment_name"]').textContent = "School code:"
        } else if (e.target.id == "user_type-2") {
            document.querySelector('label[for="establishment_name"]').textContent = "Name of restaurant/cater:"
        }
    })

    // validation
    document.querySelector("#submit").addEventListener("click", (e) => {


        if (document.querySelector("#establishment_name").value.trim() == "") {
            document.querySelector("#establishmentNameError").innerText = "Name/code cannot be blank."
            e.preventDefault()
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

if (document.querySelector("#setPassword")) {
    document.querySelector("#submit").addEventListener("click", (e) => {
        if (document.querySelector("#password").value != document.querySelector("#passwordConfirm").value) {
            e.preventDefault()
            document.querySelector(".error").innerText = "Passwords need to match"
        }
        if (document.querySelector("#password").value.length < 8) {
            e.preventDefault()
            document.querySelector(".error").innerText = "Password must be at least 8 characters long"
        }
    })
}