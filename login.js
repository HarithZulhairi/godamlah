document.getElementById('loginForm').addEventListener('submit', function (e) {
    e.preventDefault(); // Prevent form submission

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const rememberMe = document.getElementById('rememberMe').checked;

    if (email && password) {
        alert(`Welcome back! \nEmail: ${email}\nRemember Me: ${rememberMe}`);
    } else {
        alert('Please fill out all fields!');
    }
});
