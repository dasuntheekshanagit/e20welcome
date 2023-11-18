function spinWheel() {
    const wheel = document.querySelector('.wheel');
    const resultDisplay = document.getElementById('result');

    // Make an AJAX request to Flask to generate the number
    fetch('/generate_number')
        .then(response => response.json())
        .then(data => {
            const number = data.number;
            const rotation = number * 360 + 720; // Additional rotations based on the number

            wheel.style.animation = 'none'; // Reset the animation
            resultDisplay.textContent = '';

            setTimeout(() => {
                wheel.style.animation = `wheel-spin 4s ease-out forwards`; // Apply the animation
                wheel.style.transform = `rotate(${rotation}deg)`; // Apply the rotation
            }, 10); // Delay to reset animation
        })
        .catch(error => {
            console.error('Error:', error);
        });
}
