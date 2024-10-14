document.addEventListener('DOMContentLoaded', function() {
    // Size selection functionality
    var sizeBoxes = document.querySelectorAll('.size-box');
    var sizeInput = document.getElementById('size-input');

    sizeBoxes.forEach(function(box) {
        box.addEventListener('click', function() {
            sizeBoxes.forEach(function(innerBox) {
                innerBox.classList.remove('selected');
            });
            box.classList.add('selected');
            sizeInput.value = box.getAttribute('data-value');
            console.log("Selected size:", sizeInput.value); 
        });
    });

    // Add to cart form submission
    document.getElementById('add-to-cart-form').addEventListener('submit', function(event) {
        if (!sizeInput.value) {
            console.log("Size not selected. Form submission prevented."); 
            event.preventDefault();  // Prevent form submission
        } else {
            console.log("Submitting form with size:", sizeInput.value); 
        }
    });

    // Additional form validation
    const form = document.querySelector('form');
    form.addEventListener('submit', function(event) {
        const countryCode = document.getElementById('country-code').value;
        const phoneNumber = document.getElementById('phone').value;

        if (!countryCode || !phoneNumber) {
            event.preventDefault(); 
            alert('Please select a country code and enter your phone number.');
            return false;
        }
        
        return true; 
    });
});
