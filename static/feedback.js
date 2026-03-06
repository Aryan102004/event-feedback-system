document.addEventListener("DOMContentLoaded", function () {

    const form = document.querySelector(".feedback-form");

    form.addEventListener("submit", function (e) {

        const fields = form.querySelectorAll("input, select, textarea");

        let valid = true;

        fields.forEach(field => {
            if (!field.value.trim()) {
                valid = false;
                field.style.border = "2px solid red";
            } else {
                field.style.border = "1px solid #ddd";
            }
        });

        if (!valid) {
            e.preventDefault();
            alert("Please fill all required fields.");
        }

    });

});