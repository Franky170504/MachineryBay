/*------------------------- FADE ANIMATION: ABOUT SECTION HOME PAGE -------------------------*/

document.addEventListener('DOMContentLoaded', function() {
    const fadeElements = document.querySelectorAll('.fade-in');
  
    const checkVisibility = () => {
        fadeElements.forEach(el => {
            const rect = el.getBoundingClientRect();
            if (rect.top < window.innerHeight && rect.bottom > 0) {
                el.classList.add('visible');
            }
        });
    };
  
    window.addEventListener('scroll', checkVisibility);
    checkVisibility(); // Check visibility on page load
  });
  
  
  /*------------------------- COUNT UP ANIMATION: ACHIVEMENTS SECTION  HOME PAGE -------------------------*/
  
  document.addEventListener('DOMContentLoaded', function () {
    const counters = document.querySelectorAll('.count');
    const speed = 300; // Change the speed of the count
    let hasCounted = Array(counters.length).fill(false); // Track counting for each counter
  
    const updateCount = (counter) => {
        const target = +counter.getAttribute('data-target');
        const count = +counter.innerText;
  
        const increment = target / speed;
  
        if (count < target) {
            counter.innerText = Math.ceil(count + increment);
            setTimeout(() => updateCount(counter), 1);
        } else {
            counter.innerText = target + '+'; // Add the "+" after reaching the target
        }
    };
  
    const checkVisibility = () => {
        counters.forEach((counter, index) => {
            const rect = counter.getBoundingClientRect();
            // Check if the counter is in the viewport
            if (!hasCounted[index] && rect.top < window.innerHeight && rect.bottom > 0) {
                hasCounted[index] = true; // Prevent counting multiple times for this counter
                updateCount(counter);
            }
        });
    };
  
    window.addEventListener('scroll', checkVisibility);
    checkVisibility(); // Check visibility on page load
  });
  
  
/*------------------------- PRODUCT SLIDER: HOME PAGE -------------------------*/
  
  
  
  
  
  
  
  
  
  
  
  
  /*------------------------- ACCOUNT: LOG IN PAGE -------------------------*/
  
  const togglePassword = document.getElementById('togglePassword');
          const password = document.getElementById('password');
          const icon = togglePassword.querySelector('i');
  
          togglePassword.addEventListener('click', function () {
              // Toggle the password field type between 'password' and 'text'
              const type = password.getAttribute('type') === 'password' ? 'text' : 'password';
              password.setAttribute('type', type);
  
              // Toggle the icon
              icon.classList.toggle('fa-eye');
              icon.classList.toggle('fa-eye-slash');
          });
