// Hardcode the end date for the countdown (e.g., December 31, 2023 at 23:59:59)
const countdownDate = new Date("2024-01-19T23:59:59");

// Update the countdown every second
const timerElement = document.getElementById("timer");
const countdownInterval = setInterval(updateCountdown, 1000);

function updateCountdown() {
  const now = new Date().getTime();
  const distance = countdownDate - now;

  if (distance < 0) {
    clearInterval(countdownInterval);
    timerElement.innerHTML = "EXPIRED";
  } else {
    const days = Math.floor(distance / (1000 * 60 * 60 * 24));
    const hours = Math.floor(
      (distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60)
    );
    const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((distance % (1000 * 60)) / 1000);

    // Display the countdown in the element with id="timer"
    timerElement.innerHTML = `${days}D : ${hours}H : ${minutes}M : ${seconds}S`;
  }
}
