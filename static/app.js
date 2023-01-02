if (document.querySelector(".flash-message")) {
    document.querySelector(".close").addEventListener('click', (e) => {
        document.querySelector(".flash-message").classList.toggle("hide")
    })
}