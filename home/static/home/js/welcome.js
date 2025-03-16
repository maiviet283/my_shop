document.addEventListener("DOMContentLoaded", function () {
    const canvas = document.getElementById("snowCanvas");
    const ctx = canvas.getContext("2d");

    let width, height;
    function resizeCanvas() {
        width = canvas.width = window.innerWidth;
        height = canvas.height = window.innerHeight;
    }
    window.addEventListener("resize", resizeCanvas);
    resizeCanvas();

    const snowflakes = [];
    function createSnowflakes(count) {
        for (let i = 0; i < count; i++) {
            snowflakes.push({
                x: Math.random() * width,
                y: Math.random() * height,
                radius: Math.random() * 3 + 1,
                speedX: (Math.random() - 0.5) * 2,
                speedY: Math.random() * 2 + 1,
                opacity: Math.random() * 0.5 + 0.3,
            });
        }
    }

    function drawSnowflakes() {
        ctx.clearRect(0, 0, width, height);
        ctx.fillStyle = "rgba(255, 255, 255, 0.8)";
        ctx.beginPath();
        snowflakes.forEach((flake) => {
            ctx.globalAlpha = flake.opacity;
            ctx.moveTo(flake.x, flake.y);
            ctx.arc(flake.x, flake.y, flake.radius, 0, Math.PI * 2);
        });
        ctx.fill();
    }

    function updateSnowflakes() {
        snowflakes.forEach((flake) => {
            flake.y += flake.speedY;
            flake.x += flake.speedX;
            if (flake.y > height) {
                flake.y = 0;
                flake.x = Math.random() * width;
            }
        });
    }

    function animate() {
        drawSnowflakes();
        updateSnowflakes();
        requestAnimationFrame(animate);
    }

    createSnowflakes(50);
    animate();
});