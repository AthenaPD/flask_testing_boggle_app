const $response = $("#response p");
const $score = $("#score p");
const $guessForm = $("#guess-form");

class Game {
    constructor() {
        this.foundWords = [];
        this.makeGame = this.makeGame();
        this.totalScore = 0;
    }

    makeGame() {
        $guessForm.on("submit", this.handleGuessSubmit.bind(this));
        setTimeout(this.endGame.bind(this), 60000);
    }

    handleGuessSubmit(evt) {
        evt.preventDefault();
        const guess = $("#guess").val();
        if (this.foundWords.includes(guess)) {
            $response.text("This word was already found!");
            $response.removeClass("success").addClass("error");
        } else {
            this.checkGuess(guess.toLowerCase());
        }
        evt.target.reset();
    }

    async checkGuess(guess) {
        const response = await axios.post("http://127.0.0.1:5000/play", {game: "on", guess});
        if (response.data.result === "ok") {
            $response.text("Good Job!");
            $response.removeClass("error").addClass("success");
            this.totalScore += guess.length;
            this.foundWords.push(guess);
            $score.text(`Score: ${this.totalScore}`);
        } else if (response.data.result === "not-on-board") {
            $response.text("Your word is NOT on the board. Please try again!");
            $response.removeClass("success").addClass("error");
        } else {
            $response.text("This is NOT a valid word. Please try again!");
            $response.removeClass("success").addClass("error");
        }
    }

    async endGame() {
        $guessForm.hide();
        $response.text("Good game!");
        $response.removeClass("error").addClass("success");

        const response = await axios.post("http://127.0.0.1:5000/play", {game: "off", score: this.totalScore});
    }
}

new Game();
