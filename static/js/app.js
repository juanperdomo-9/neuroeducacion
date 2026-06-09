const navbar = document.querySelector('#navbar')

window.addEventListener('scroll', () => {

    if (window.scrollY > 50) {

        navbar.classList.add(
            'bg-black/50',
            'backdrop-blur-xl',
            'border-b',
            'border-white/10'
        )

    } else {

        navbar.classList.remove(
            'bg-black/50',
            'backdrop-blur-xl',
            'border-b',
            'border-white/10'
        )

    }

})

const reveals = document.querySelectorAll(".reveal");

const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {

        if (entry.isIntersecting) {

            entry.target.classList.add("revealed");

        }

    });

}, {
    threshold: 0.1,
});

reveals.forEach((el, index) => {

    el.style.transitionDelay = `${index * 80}ms`;

    observer.observe(el);

});