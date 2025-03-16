document.addEventListener("DOMContentLoaded", function() {
    for (let i = 0; i < 30; i++) {
        let particle = document.createElement("div");
        particle.classList.add("particle");
        document.body.appendChild(particle);
        
        let x = Math.random() * window.innerWidth;
        let y = Math.random() * window.innerHeight;
        let delay = Math.random() * 2;
        
        particle.style.left = `${x}px`;
        particle.style.top = `${y}px`;
        particle.style.animationDelay = `${delay}s`;
        
        setTimeout(() => {
            particle.remove();
        }, 3000);
    }
});
