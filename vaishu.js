
// LIKE BUTTON FUNCTION

function likeTutor(tutor) {

    let likes = JSON.parse(
        localStorage.getItem("tutorLikes") || "{}"
    );

    likes[tutor] = (likes[tutor] || 0) + 1;

    localStorage.setItem(
        "tutorLikes",
        JSON.stringify(likes)
    );

    document.getElementById(tutor + "-count").textContent =
        likes[tutor];
}

// DISPLAY SAVED LIKES

function displayLikes() {

    let likes = JSON.parse(
        localStorage.getItem("tutorLikes") || "{}"
    );

    document.getElementById("math-count").textContent =
        likes.math || 0;

    document.getElementById("programming-count").textContent =
        likes.programming || 0;
}

// OPEN LOGIN

function openLogin() {
    document.getElementById("authModal").style.display = "flex";
    showLogin();
}

// CLOSE LOGIN

function closeLogin() {
    document.getElementById("authModal").style.display = "none";
}

// SHOW REGISTER

function showRegister() {
    document.getElementById("registerForm").style.display = "block";
    document.getElementById("loginForm").style.display = "none";
    document.getElementById("message").textContent = "";
}

// SHOW LOGIN

function showLogin() {
    document.getElementById("registerForm").style.display = "none";
    document.getElementById("loginForm").style.display = "block";
    document.getElementById("message").textContent = "";
}

// REGISTER FUNCTION

function register(event) {

    event.preventDefault();

    let name = document.getElementById("regName").value.trim();
    let email = document.getElementById("regEmail").value.trim().toLowerCase();
    let password = document.getElementById("regPassword").value;

    let users = JSON.parse(
        localStorage.getItem("educareUsers") || "{}"
    );

    if (users[email]) {
        document.getElementById("message").textContent =
            "Email already registered!";
        return;
    }

    users[email] = {
        name: name,
        password: password
    };

    localStorage.setItem(
        "educareUsers",
        JSON.stringify(users)
    );

    alert("Registration successful! Please login.");

    event.target.reset();
    showLogin();
}

// LOGIN FUNCTION

function login(event) {

    event.preventDefault();

    let email = document.getElementById("loginEmail").value.trim().toLowerCase();
    let password = document.getElementById("loginPassword").value;

    let users = JSON.parse(
        localStorage.getItem("educareUsers") || "{}"
    );

    let user = users[email];

    if (user && user.password === password) {

        localStorage.setItem("educareCurrentUser", email);

        document.getElementById("welcomeUser").textContent =
            "Hello, " + user.name;

        document.getElementById("dashboard").style.display = "block";

        closeLogin();

        document.getElementById("loginEmail").value = "";
        document.getElementById("loginPassword").value = "";

        window.location.hash = "dashboard";

    } else {

        document.getElementById("message").textContent =
            "Invalid email or password!";
    }
}

// LOGOUT FUNCTION

function logout() {

    localStorage.removeItem("educareCurrentUser");

    document.getElementById("dashboard").style.display = "none";

    alert("Logged out successfully!");
}

// RESTORE LOGIN AND LIKES

window.addEventListener("DOMContentLoaded", function() {

    displayLikes();

    let email = localStorage.getItem("educareCurrentUser");

    let users = JSON.parse(
        localStorage.getItem("educareUsers") || "{}"
    );

    if (email && users[email]) {

        document.getElementById("welcomeUser").textContent =
            "Hello, " + users[email].name;

        document.getElementById("dashboard").style.display = "block";
    }
});

// CLOSE POPUP WHEN CLICKING OUTSIDE

document.getElementById("authModal").addEventListener("click", function(event) {

    if (event.target === this) {
        closeLogin();
    }
});
