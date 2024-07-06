// Sidebar toggler
const toggler = document.querySelector(".btn");
const sidebar = document.querySelector("#sidebar");

toggler.addEventListener("click", function () {
  sidebar.classList.toggle("collapsed");
});

if (window.innerWidth > 768) {
  sidebar.classList.remove("collapsed");
}

window.addEventListener("resize", function () {
  if (window.innerWidth > 768) {
    sidebar.classList.remove("collapsed");
  } else {
    sidebar.classList.add("collapsed");
  }
});

let touchstartX = 0;
let touchendX = 0;
const swipeThreshold = 100

sidebar.addEventListener('touchstart', function(event) {
    touchstartX = event.changedTouches[0].screenX;
}, false);

sidebar.addEventListener('touchend', function(event) {
    touchendX = event.changedTouches[0].screenX;
    handleGesture();
}, false);

document.addEventListener('touchstart', function(event) {
    const targetElement = event.target;
    if (targetElement && targetElement.closest('.table-responsive')) {
        return;
    }
    touchstartX = event.changedTouches[0].screenX;
}, false);

document.addEventListener('touchend', function(event) {
    const targetElement = event.target;
    if (targetElement && targetElement.closest('.table-responsive')) {
        return;
    }
    touchendX = event.changedTouches[0].screenX;
    handleGesture();
}, false);

function handleGesture() {
    const touchDistance = touchendX - touchstartX;

    if (Math.abs(touchDistance) > swipeThreshold) {
        if (touchDistance < 0) {
            // Swiped left
            if (!sidebar.classList.contains("collapsed")) {
                sidebar.classList.add("collapsed");
            }
        }
        if (touchDistance > 0) {
            // Swiped right
            if (sidebar.classList.contains("collapsed")) {
                sidebar.classList.remove("collapsed");
            }
        }
    }
}