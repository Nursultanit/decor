document.addEventListener('DOMContentLoaded', () => {

    // HEADER SCROLL EFFECT

    const header = document.querySelector('.header');

    window.addEventListener('scroll', () => {

        if(window.scrollY > 50){

            header.style.background = 'rgba(255,255,255,0.95)';
            header.style.boxShadow = '0 10px 30px rgba(0,0,0,0.08)';

        }else{

            header.style.background = 'rgba(255,255,255,0.85)';
            header.style.boxShadow = 'none';

        }

    });



    // CARD ANIMATION

    const cards = document.querySelectorAll('.card');

    cards.forEach(card => {

        card.addEventListener('mouseenter', () => {

            card.style.transform = 'translateY(-12px) scale(1.02)';

        });

        card.addEventListener('mouseleave', () => {

            card.style.transform = 'translateY(0) scale(1)';

        });

    });



    // SMOOTH SCROLL

    const links = document.querySelectorAll('a[href^="#"]');

    links.forEach(link => {

        link.addEventListener('click', function(e){

            e.preventDefault();

            const target = document.querySelector(this.getAttribute('href'));

            if(target){

                target.scrollIntoView({
                    behavior:'smooth'
                });

            }

        });

    });



    // FADE ANIMATION

    const observer = new IntersectionObserver(entries => {

        entries.forEach(entry => {

            if(entry.isIntersecting){

                entry.target.classList.add('show');

            }

        });

    }, {
        threshold:0.2
    });



    const hiddenElements = document.querySelectorAll(
        '.card, .review-card, .adv-card, .cta-box'
    );

    hiddenElements.forEach(el => {

        el.classList.add('hidden');

        observer.observe(el);

    });



    // WHATSAPP BUTTON EFFECT

    const buttons = document.querySelectorAll('.btn, .btn-small');

    buttons.forEach(btn => {

        btn.addEventListener('mouseenter', () => {

            btn.style.transform = 'scale(1.05)';

        });

        btn.addEventListener('mouseleave', () => {

            btn.style.transform = 'scale(1)';

        });

    });

});