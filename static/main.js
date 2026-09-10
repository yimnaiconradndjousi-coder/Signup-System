const showOrHidePassword = document.getElementById('show-or-hide-password');
const userNameInput = document.getElementById('username');
const passwordInput = document.getElementById('password');
const emailIput = document.getElementById('email');
const passwordError = document.getElementById('password-error');
const usernameError = document.getElementById('username-error');
const emailError = document.getElementById('email-error');
const hr = document.querySelector('.hr');
const signupForm = document.querySelector('.signup-form');
const signupBtn = document.getElementById('signup-btn');

// Hide or Show logic
showOrHidePassword.addEventListener('click', function(e) {   
    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        showOrHidePassword.src = '../src/hide-password.png';
    } else if (passwordInput.type === 'text') {
        passwordInput.type = 'password';
        showOrHidePassword.src = '../src/show-password.png';
    }
});

const isPasswordValid = (userName == '') ? true : false

function errorDisplay(btn) {
    btn.addEventListener('click', function(e) {
        e.preventDefault();
        let userName = null;
        userName = (signupForm) ? userNameInput.value.trim() : null;
        const password = passwordInput.value;
        const email = emailIput.value;

        function insertErrorMessage(inputError, hrline) {
            hrline.style.marginBottom = '5px';
            inputError.style.color = 'red';
            inputError.style.fontSize = '14px';
            inputError.style.margin = '5px';
        };

        if (password.length < 3) {
            passwordError.textContent = 'Password must be at least 8 characters.';
            insertErrorMessage(passwordError, hr);

            setTimeout( function() {
                    passwordError.textContent = '';
            }, 2000)
        };

        if (userName == '') {
            if (usernameError) {
                usernameError.textContent = 'Please enter your username.';
                insertErrorMessage(usernameError, hr);

                setTimeout( function() {
                        usernameError.textContent = '';
                }, 2000)
            }
        }

        if (email == '') {
            if (emailError) {
                emailError.textContent = 'Please enter your username.';
                insertErrorMessage(emailError, hr);

                setTimeout( function() {
                        emailError.textContent = '';
                }, 2000)
            }
        }
    });          
}

