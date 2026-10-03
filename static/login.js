const showOrHidePassword = document.getElementById('show-or-hide-password');
const passwordInput = document.getElementById('password');
const emailIput = document.getElementById('email');
const passwordError = document.getElementById('password-error');
const emailError = document.getElementById('email-error');
const hr = document.querySelector('.hr');
const loginForm = document.getElementById('login-form');
const loginBtn = document.getElementById('login-btn');
const loginURL = "http://localhost:8080/api/auth/login"

showOrHidePassword.addEventListener('click', function(e) {   
    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        showOrHidePassword.src = '../src/hide-password.png';
    } else {
        passwordInput.type = 'password';
        showOrHidePassword.src = '../src/show-password.png';
    }
});

async function postUserData(url, data) {
    try {
        const response = await fetch(url, {
            method:"POST",
            credentials: "include",
            headers: {
                "Content-Type":"application/json"
            },
            body: JSON.stringify(data)
        })
        
        const result = await response.json();

        if (response.status === 400) {
            alert("Something Went wrong")
            console.error("Invalid Email or password.")
        }

        if (response.ok) {
            window.location.href = '/templates/index.html';
        }

        if (!response.ok) {
            throw new Error(`Status ${response.status}, ${result.message}`)
        }

        console.log("Saved:", result.message);
        // window.location.href = '/templates/index.html';
    } catch(error) {
        console.error("Signup failed:", error.message);
    }
}

function insertErrorMessage(inputError, hrline, msg) {
    inputError.textContent = msg;
    hrline.style.marginBottom = '5px';
    inputError.style.color = 'red';
    inputError.style.fontSize = '14px';
    inputError.style.margin = '5px';

    setTimeout( () => {
            inputError.textContent = '';
    }, 2500)
}

loginBtn.addEventListener('click', function(e) {
    e.preventDefault();
    const password = passwordInput.value;
    const email = emailIput.value.trim();

    let isEmailValid = email !== '';
    let isPasswordValid = password.length >= 8;
    
    if (!isPasswordValid) {
        insertErrorMessage(passwordError, hr, "Password must be at least 8 characters.");
    };

    if (!isEmailValid) {
        insertErrorMessage(emailError, hr, "Please enter a valid email.");
    }

    if (isEmailValid && isPasswordValid) {
        const user = {
            email: email,
            password: password
        }
        postUserData(loginURL, user);
    }
});          
