// Ensure the DOM is fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Get references to DOM elements
    const paymentForm = document.getElementById('payment-form');
    const paymentMethodInputs = document.querySelectorAll('input[name="payment_method"]');
    const cardElementContainer = document.getElementById('card-element-container');
    
    // Initialize Stripe
    const stripe = Stripe('your-publishable-key-here');
    const elements = stripe.elements();
    const cardElement = elements.create('card');
    cardElement.mount('#card-element');
    
    // Function to toggle card element visibility
    function toggleCardElement() {
        const selectedPaymentMethod = document.querySelector('input[name="payment_method"]:checked').value;
        if (selectedPaymentMethod === 'Online Payment') {
            cardElementContainer.classList.remove('hidden');
        } else {
            cardElementContainer.classList.add('hidden');
        }
    }

    // Attach change event listeners to payment method inputs
    paymentMethodInputs.forEach(input => {
        input.addEventListener('change', toggleCardElement);
    });

    // Initial call to set the correct visibility based on the default selected payment method
    toggleCardElement();

    // Handle form submission
    paymentForm.addEventListener('submit', function(event) {
        const selectedPaymentMethod = document.querySelector('input[name="payment_method"]:checked').value;

        if (selectedPaymentMethod === 'Online Payment') {
            event.preventDefault(); // Prevent form submission for online payment

            stripe.createToken(cardElement).then(function(result) {
                if (result.error) {
                    // Inform the user if there was an error
                    const errorElement = document.getElementById('card-errors');
                    errorElement.textContent = result.error.message;
                } else {
                    // Send the token to your server
                    stripeTokenHandler(result.token);
                }
            });
        } else {
            // Allow form submission for other payment methods
            paymentForm.submit();
        }
    });

    // Function to handle the Stripe token
    function stripeTokenHandler(token) {
        // Insert the token ID into the form so it gets submitted to the server
        const hiddenInput = document.createElement('input');
        hiddenInput.setAttribute('type', 'hidden');
        hiddenInput.setAttribute('name', 'stripeToken');
        hiddenInput.setAttribute('value', token.id);
        paymentForm.appendChild(hiddenInput);

        // Submit the form
        paymentForm.submit();
    }
});
