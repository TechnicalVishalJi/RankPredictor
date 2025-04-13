window.onload = function() {
    const intro = document.querySelector(".intro");
    const children = Array.from(intro.children); // Use .children to get only element nodes
    children.forEach(node => {
        node.style.opacity = 0;
        node.style.transform = "translateY(10px)"; // Corrected property name
    });
    intro.style.display = "block";
    intro.style.opacity = 1;

    let timeline = gsap.timeline();
    children.forEach(node => {
        timeline.to(node, {opacity: 1, y: "-=10px", duration: 0.5, ease: "power2.out"});
    });
}

document.getElementById("startPrediction").addEventListener("click", () => {
    const intro = document.querySelector(".intro");
    // intro.style.position = "absolute";
    const predictor = document.querySelector(".predictor .outer");

    // Hide the intro and animate the predictor

    let timeline = gsap.timeline();
    timeline.to(intro, {
            duration: 0.5,
            // x: "45vw",
            // opacity: 0,
            // width: "0%",
            scale: 0,
            ease: "power2.out",
            onComplete: () => {
                intro.style.display = "none"; // Hide intro after animation
            }
        })
        .fromTo(predictor,{
            opacity: 0,
            scale: 0,
            width: "20%",
        },
        {
            display: "flex",
            opacity: 1,
            scale: 1,
            duration: 0.5,
            ease: "power2.out",
        });
    if(!isMobileDevice()) {
        timeline.to(predictor, {
            duration: 1,
            width: "80%",
            ease: "power4.out",
        });
    }else{
        timeline.to(predictor, {
            duration: 1,
            width: "90%",
            ease: "power4.out",
        });
    }
});

function isMobileDevice() {
    return window.innerWidth <= 768;
}