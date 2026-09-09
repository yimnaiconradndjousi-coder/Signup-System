const serverURL = "http://localhost:8080/signup"
let user = {
    username:"YImnai Conrad",
    email:"Yims@gmail.com",
    password:"admin123"
}


async function postData(url, data) {
    const response = await fetch(url, {
        method:"POST",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify(data)
    })

    if (!response.ok) throw new Error(`Status ${response.status}`);
    const result = await response.json();
    console.log("Saved:", result);
}

postData(serverURL, user)