function animateSeeds() {
    const numberOfSeeds = 30;
    const seedRadius = 20; // Half of the image width
    const container = d3.select(".dandelions");

    const seedData = Array.from({ length: numberOfSeeds }, (_, i) => {
        const initialX = container.node().offsetWidth * 0.7;
        const initialY = container.node().offsetWidth * 0.6;
        const angle = Math.random() * (55 - (-30)) + (-30); // Random angle between -30 and 45 degrees
        const radianAngle = (angle * Math.PI) / 180;
        const vx = Math.cos(radianAngle) * (Math.random() * 2 - 1);
        const vy = Math.sin(radianAngle) * (Math.random() * 2 - 1);
        const animationDuration = Math.random() * (8000 - 4000) + 4000; // Random duration between 6000 and 10000 milliseconds

        return {
            id: i,
            x: initialX,
            y: initialY,
            vx: vx,
            vy: vy,
            angle: angle,
            animationDuration: animationDuration
        };
    });

    const svg = container
        .append("svg")
        .attr("width", "100%")
        .attr("height", "100%");

    const seeds = svg
        .selectAll(".seed")
        .data(seedData)
        .enter()
        .append("image")
        .attr("class", "seed")
        .attr("xlink:href", "images/seed.png") 
        .attr("width", 40)
        .attr("height", 40)
        .attr("x", d => d.x - seedRadius) 
        .attr("y", d => d.y - seedRadius)
        .attr("transform", d => `rotate(${d.angle},${d.x},${d.y})`) // Rotate the image based on the random angle
        .style("opacity", 0.8); 

    function animateSeeds() {
        seeds
            .transition()
            .duration(d => d.animationDuration)
            .delay((_, i) => i * 200)
            .attrTween("x", bounceX)
            .attrTween("y", bounceY)
            .on("end", animateSeeds);
    }

    animateSeeds();

    function bounceX(d) {
        return function (t) {
            d.x += d.vx;
            d.vx *= (d.x > container.node().offsetWidth - seedRadius || d.x < seedRadius) ? -1 : 1;
            return d.x - seedRadius;
        };
    }

    function bounceY(d) {
        return function (t) {
            d.y += d.vy;
            d.vy *= (d.y > container.node().offsetHeight - seedRadius || d.y < seedRadius) ? -1 : 1;
            return d.y - seedRadius;
        };
    }
}
