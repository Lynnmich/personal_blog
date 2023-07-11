const slides = document.querySelectorAll('.slide');
let currentSlide = 0;

function showSlide() {
  slides[currentSlide].classList.add('active');
}

function hideSlide() {
  slides[currentSlide].classList.remove('active');
}

function nextSlide() {
  hideSlide();
  currentSlide = (currentSlide + 1) % slides.length;
  showSlide();
}

showSlide();

setInterval(nextSlide, 5000);
