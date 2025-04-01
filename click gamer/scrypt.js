let score = 0;

document.getElementById("clickButton").addEventListener("click", function() {
    score++;
    document.getElementById("score").textContent = score;
});
