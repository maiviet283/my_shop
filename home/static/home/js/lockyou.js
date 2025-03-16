document.addEventListener("DOMContentLoaded", function() {
    for (let i = 0; i < 20; i++) {
        let bubble = document.createElement("div");
        bubble.classList.add("floating-bubble");
        document.body.appendChild(bubble);
        
        let x = Math.random() * window.innerWidth;
        let y = Math.random() * window.innerHeight;
        let delay = Math.random() * 5;
        
        bubble.style.left = `${x}px`;
        bubble.style.top = `${y}px`;
        bubble.style.animationDelay = `${delay}s`;
        
        setTimeout(() => {
            bubble.remove();
        }, 5000);
    }
});