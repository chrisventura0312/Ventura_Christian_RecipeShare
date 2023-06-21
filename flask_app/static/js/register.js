const passwordField = document.getElementById('password');
const showPasswordCheckbox = document.getElementById('show-password-checkbox');
const showConfrimPasswordCheckbox = document.getElementById('show-confirm-password-checkbox');
const confirmPasswordField = document.getElementById('confirm-password');
    
showPasswordCheckbox.addEventListener('change', function () {
    if (showPasswordCheckbox.checked) {
        passwordField.type = 'text';
        } else {
            passwordField.type = 'password';
        }
    });

showConfrimPasswordCheckbox.addEventListener('change', function () {
    if (showConfrimPasswordCheckbox.checked) {
        confirmPasswordField.type = 'text';
        } else {
            confirmPasswordField.type = 'password';
        }
    });