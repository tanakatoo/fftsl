const BASE_URL = "http://localhost:5000/api"

document.querySelector("#searchBtn").addEventListener("click", (e) => {
    e.preventDefault()
    let criteria = document.querySelector("#search").value
    res = searchRes(criteria)
})

async function searchRes(criteria) {
    const res = await axios({
        url: `${BASE_URL}/search`,
        method: "GET",
        params: {
            s: criteria
        }
    })
    console.log(res)
}