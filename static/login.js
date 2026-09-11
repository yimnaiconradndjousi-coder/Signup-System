const showOrHidePassword = document.getElementById('show-or-hide-password');
const passwordInput = document.getElementById('password');
const emailIput = document.getElementById('email');
const passwordError = document.getElementById('password-error');
const emailError = document.getElementById('email-error');
const hr = document.querySelector('.hr');
const loginBtn = document.getElementById('login-btn');
const loginURL = "http://localhost:8080/login"

showOrHidePassword.addEventListener('click', function(e) {   
    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        showOrHidePassword.src = '../src/hide-password.png';
    } else {
        passwordInput.type = 'password';
        showOrHidePassword.src = '../src/show-password.png';
    }
});

function insertErrorMessage(inputError, hrline) {
    hrline.style.marginBottom = '5px';
    inputError.style.color = 'red';
    inputError.style.fontSize = '14px';
    inputError.style.margin = '5px';
};

async function postUserData(url, data) {
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


loginBtn.addEventListener('click', function(e) {
    e.preventDefault();
    const password = passwordInput.value;
    const email = emailIput.value.trim();

    let isEmailValid = (email == '') ? true: false;
    let isPasswordValid = (password.length < 3) ? true : false;
    
    if (password.length < 3) {
        passwordError.textContent = 'Password must be at least 8 characters.';
        insertErrorMessage(passwordError, hr);

        setTimeout( () => {
                passwordError.textContent = '';
        }, 2500)
    };

    if (email == '') {
        if (emailError) {
            emailError.textContent = 'Please enter your email.';
            insertErrorMessage(emailError, hr);

            setTimeout( () => {
                    emailError.textContent = '';
            }, 2500)
        }
    }

    if (!isEmailValid && !isPasswordValid) {
        const user = {
            email: email,
            password: password
        }

        postUserData(loginURL, user);
    }

});          


