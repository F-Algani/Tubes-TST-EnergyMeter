// Animated
let wrapper = document.querySelector('.wrapper'),
signUpLink = document.querySelector('.link .signup-link'),
signInLink = document.querySelector('.link .signin-link');
signInForm = document.querySelector('.form-container .signInForm');
signUpForm = document.querySelector('.form-container .signUpForm');

signUpLink.addEventListener('click', () => {
    wrapper.classList.add('animated-signin');
    wrapper.classList.remove('animated-signup');
});

signInLink.addEventListener('click', () => {
    wrapper.classList.add('animated-signup');
    wrapper.classList.remove('animated-signin');
});

signInForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const username = document.getElementById("username-signin").value;
    const password = document.getElementById("password-signin").value;

    try {
        const resp = await fetch("https://energymeter-18221108.azurewebsites.net/token", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
            },
            body: `username=${username}&password=${password}`,
        });
        if (resp.ok) {
            window.location.href = "https://energymeter-18221108.azurewebsites.net/docs";
            document.getElementById("username-signin").value = "";
            document.getElementById("password-signin").value = "";
        }
        else {
            const dataError = await resp.json();
            console.error("Error: Invalid Username or Password");
        }
    }
    catch (error) {
        console.error("Error occured during signing in", error.message);
    }
});

signUpForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const username = document.getElementById("username-signup").value;
    const fullname = document.getElementById("fullname-signup").value;
    const email = document.getElementById("email-signup").value;
    const password = document.getElementById("password-signup").value;

    const formData = new FormData();
    formData.append("username", username);
    formData.append("full_name", fullname);
    formData.append("email", email);
    formData.append("password", password);

    try {
        const resp = await fetch("https://energymeter-18221108.azurewebsites.net/register", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body: new URLSearchParams(formData),
        });
        if (resp.ok) {
            wrapper.classList.add('animated-signup');
            wrapper.classList.remove('animated-signin');

            document.getElementById("username-signup").value = "";
            document.getElementById("fullname-signup").value = "";
            document.getElementById("email-signup").value = "";
            document.getElementById("password-signup").value = "";
        }
        else {
            console.error("Registration Failed. Please Try Again");
        }
    }
    catch (error) {
        console.error("Error occured during registration", error.message);
    }
})