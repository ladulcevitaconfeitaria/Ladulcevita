// Basic JavaScript interactions for CLUBE LA DULCE VITA

document.addEventListener("DOMContentLoaded", function() {
    console.log("Clube La Dulce Vita site loaded.");

    // Example: Basic form validation (e.g., password confirmation)
    const registerForm = document.querySelector("form[action*=\"/register\"]");
    if (registerForm) {
        registerForm.addEventListener("submit", function(event) {
            const password = registerForm.querySelector("#password");
            const confirmPassword = registerForm.querySelector("#confirm_password");

            if (password && confirmPassword && password.value !== confirmPassword.value) {
                alert("As senhas não coincidem!");
                event.preventDefault(); // Prevent form submission
            }
            // Add more complex validation as needed
        });
    }

    // Add other interactions here, like:
    // - Mobile menu toggle
    // - Simple animations or effects
    // - Client-side input formatting (e.g., phone number mask)

});

