let slideIndex = 1;

function showSlides(n) {
    let slides = document.getElementsByClassName("slide");
    if (slides.length === 0) return;
    if (n > slides.length) { slideIndex = 1; }
    if (n < 1) { slideIndex = slides.length; }
    for (let i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
    }
    slides[slideIndex - 1].style.display = "block";
}

function moveSlide(n) {
    showSlides(slideIndex += n);
}

showSlides(slideIndex);