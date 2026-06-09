document.addEventListener(
    'DOMContentLoaded',
    () => {

        const reveals = document.querySelectorAll(
            '.reveal'
        );

        const observer = new IntersectionObserver(

            (entries) => {

                entries.forEach((entry) => {

                    if (entry.isIntersecting) {

                        entry.target.classList.add(
                            'revealed'
                        );

                    }

                });

            },

            {
                threshold: 0.12,
            }

        );

        reveals.forEach((el) => {

            observer.observe(el);

        });

    }
);