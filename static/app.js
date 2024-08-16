const $response = $("#response p");
const $score = $("#score p");
const $guessForm = $("#guess-form");
let totalScore = 0;

$guessForm.on("submit", handleGuessSubmit);

function handleGuessSubmit(evt) {
    evt.preventDefault();
    const guess = $("#guess").val();
    checkGuess(guess.toLowerCase());
    evt.target.reset();
}

async function checkGuess(guess) {
    const response = await axios.post("http://127.0.0.1:5000/play", {game: "on", guess});
    if (response.data.result === "ok") {
        $response.text("Good Job!");
        $response.removeClass("error").addClass("success");
        totalScore += guess.length;
        $score.text(`Score: ${totalScore}`);
    } else if (response.data.result === "not-on-board") {
        $response.text("Your word is NOT on the board. Please try again!");
        $response.removeClass("success").addClass("error");
    } else {
        $response.text("This is NOT a valid word. Please try again!");
        $response.removeClass("success").addClass("error");
    }
}

async function endGame() {
    $guessForm.hide();
    $response.text("Good game!");

    const response = await axios.post("http://127.0.0.1:5000/play", {game: "off", score: totalScore});
}

// setTimeout(endGame, 60000);
