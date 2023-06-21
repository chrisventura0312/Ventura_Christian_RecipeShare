const passwordField = document.getElementById('password');
const showPasswordCheckbox = document.getElementById('show-password-checkbox');

showPasswordCheckbox.addEventListener('change', function() {
    if (showPasswordCheckbox.checked) {
        passwordField.setAttribute('type', 'text');
    } else {
        passwordField.setAttribute('type', 'password');
    }
});