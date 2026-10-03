const showOrHidePassword = document.getElementById('show-or-hide-password');
const userNameInput = document.getElementById('username');
const passwordInput = document.getElementById('password');
const emailIput = document.getElementById('email');
const passwordError = document.getElementById('password-error');
const usernameError = document.getElementById('username-error');
const emailError = document.getElementById('email-error');
const hr = document.querySelector('.hr');
const signupForm = document.querySelector('form');
const signupBtn = document.getElementById('signup-btn');
const signupURL = "http://localhost:8080/api/register"

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
            credentials:'include',
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

        if (response.status === 201) {
            const result = await response.json();
            alert('Signup successful. Please log in.');
            console.log("Saved:", result.message);
        }

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

signupForm.addEventListener('submit', function(e) {
    e.preventDefault();
    const userName = userNameInput.value.trim();
    const password = passwordInput.value;
    const email = emailIput.value.trim();

    let isUsernameValid = userName !== '';
    let isEmailValid = email !== '';
    let isPasswordValid = password.length >= 8;

    if (password.length < 8) {
        insertErrorMessage(passwordError, hr, "Password must be at least 8 characters.")
    };

    if (userName == '') {
        insertErrorMessage(usernameError, hr, "Please enter a valid username.")
    }

    if (email == '') {
        insertErrorMessage(emailError, hr, "Please enter a valid email.")
    }

    if (isUsernameValid && isEmailValid && isPasswordValid) {
        const user = {
            username: userName,
            email: email,
            password: password
        }

        postUserData(signupURL, user);
    }

});          