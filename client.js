const serverURL = "http://localhost:8080/signup"
let user = {
    username:"YImnai",
    email:"conradnyc@zohomail.com",
    password:"admin123"
}

async function postData(url, data) {
    try {
        const response = await fetch(url, {
            method:"POST",
            headers: {
                "Content-Type":"application/json"
            },
            body: JSON.stringify(data)
        })

        if (!response.ok) {
            const error = await response.json();
            throw new Error(
                `Status ${response.status}, ${error.message}`
            );
        }

        const result = await response.json();
        console.log("Saved:", result.message);
    } catch(error) {
        console.error("Signup failed:", error.message);
    }

}

postData(serverURL, user);