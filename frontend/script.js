let mode = "login"; // default mode

const form = document.getElementById("auth-form");
const messageBox = document.getElementById("message");
const usernameField = document.getElementById("username-field");
const formTitle = document.getElementById("form-title");
const submitBtn = document.getElementById("submit-btn");
const toggleLink = document.getElementById("toggle-link");
const toggleAction = document.getElementById("toggle-action");

// --------------------------
// Toggle between Login / Register
// --------------------------
toggleLink.addEventListener("click", () => {
    if (mode === "login") {
        mode = "register";
        usernameField.classList.remove("hidden");
        formTitle.textContent = "Register";
        submitBtn.textContent = "Register";
        toggleAction.textContent = "Already have an account?";
        toggleLink.textContent = "Login";
    } else {
        mode = "login";
        usernameField.classList.add("hidden");
        formTitle.textContent = "Login";
        submitBtn.textContent = "Login";
        toggleAction.textContent = "Don't have an account?";
        toggleLink.textContent = "Register";
    }
});

// --------------------------
// Form Submit
// --------------------------
form.addEventListener("submit", async (e) => {
    e.preventDefault();
    messageBox.textContent = "";

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const username = document.getElementById("username").value;

    let url = "";
    let body = {};

    if (mode === "login") {
        url = "http://127.0.0.1:8000/login";
        body = { email, password };
    } else {
        url = "http://127.0.0.1:8000/register";
        body = { username, email, password };
    }

    try {
        const res = await fetch(url, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(body)
        });

        const data = await res.json();

        if (!res.ok) {
            messageBox.style.color = "red";
            messageBox.textContent = data.detail || "Error occurred";
            return;
        }

        messageBox.style.color = "green";
        messageBox.textContent = data.message;

    } catch (err) {
        messageBox.style.color = "red";
        messageBox.textContent = "Server error";
    }
});
