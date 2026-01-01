# Hangmn Game

# A simple Hangman game implemented with Gradio for the web interface.
# The game randomly selects a word from a predefined list and provides hints.
# Players can guess letters, and the game tracks the number of trials left.

# import necessary libraries
import gradio as gr
import random

# Hangman game logic
# Define the Hangman class
class Hangman:
    def __init__(self):
        self.answers = {
            "SUN": "That star in our solar system",
            "SNAKE": "A type of reptile.",
            "LAKE": "It's bigger than a pond but smaller than an ocean.",
            "HOUSE": "Built on a foundation",
            "BALL": "Used in many sports",
            "BOOK": "Something you can read",
            "RIVER": "Flows to the sea",
            "MOUNTAIN": "A large natural elevation of the earth's surface",
            "COMPUTER": "An electronic device for storing and processing data",
            "PYTHON": "A popular programming language",
            "GUITAR": "A stringed musical instrument",
            "ELEPHANT": "The largest land animal",
            "BICYCLE": "A vehicle with two wheels",
            "TELESCOPE": "Used to observe distant objects",
            "KANGAROO": "A marsupial from Australia",
            "UMBRELLA": "Used for protection against rain",
            "CANDY": "A sweet treat",
            "ISLAND": "Land surrounded by water",
            "JUNGLE": "A dense forest in a tropical region",
            "VOLCANO": "A mountain that erupts",
            "ZEBRA": "An animal with black and white stripes",
            "PENGUIN": "A flightless bird that lives in cold climates",
            "ASTRONAUT": "A person who travels in space",
            "BUBBLE": "A thin sphere of liquid enclosing air or another gas",
            "DOLPHIN": "A highly intelligent marine mammal",
            "FOSSIL": "Preserved remains of ancient organisms",
            "GALAXY": "A system of millions or billions of stars",
            "HARMONY": "A pleasing arrangement of parts",
            "INSECT": "A small arthropod animal",
            "JOURNAL": "A daily record of news and events",
            "PYRAMID": "A monumental structure with a square or triangular base",
            "QUARTZ": "A hard, crystalline mineral",
            "RAINBOW": "An arc of colors visible in the sky",
            "PLANET": "A celestial body orbiting a star",
            "OCEAN": "A large body of salt water",
            "FOREST": "A large area covered chiefly with trees and undergrowth",
            "DESERT": "A barren area of landscape",
            "PALINDROME": "A word that reads the same backward as forward",
            "ECLIPSE": "An obscuring of the light from one celestial body by another",
            "SYMMETRY": "Balanced proportions on opposite sides",
            "LUMINOUS": "Emitting light",
            "MIRROR": "A reflective surface",
            "RHYTHM": "A strong, regular, repeated pattern of movement or sound",
            "PAPER": "Material made from wood pulp",
            "CLOCK": "A device used to tell time",
            "BRIDGE": "A structure built to span physical obstacles",
            "LOCKET": "A small ornamental case for a picture or keepsake",
            "MAGNET": "An object that attracts iron and steel",
            "OTTAWA": "Capital city of Canada",
            "BERLIN": "Capital city of Germany",
            "DUBLIN": "Capital city of Ireland",
            "MADRID": "Capital city of Spain",
            "VIENNA": "Capital city of Austria",
            "OUAGADOUGOU": "Capital city of Burkina Faso"
        }
        self.answer_words = list(self.answers.keys())
        self.reset_game()
    
    # Reset the game state
    def reset_game(self):
        self.answer = random.choice(self.answer_words)
        self.hint = self.answers[self.answer]
        self.answer_len = len(self.answer)
        self.guess_lst = ["_"] * self.answer_len
        self.n_trials = int(self.answer_len * 1.5)
        self.count = 0
        self.finished = False
        self.comment_of_guess = []

    # Process a letter guess
    def make_guess(self, letter):
        if self.finished:
            return "Game over. Please start a new game.", " ".join(self.guess_lst), self.n_trials - self.count

        letter = letter.strip().upper()
        if not letter or len(letter) != 1 or not letter.isalpha():
            return "Please enter a single valid letter.", " ".join(self.guess_lst), self.n_trials - self.count
        
        if letter in self.guess_lst:
            return f"You already guessed {letter}.", " ".join(self.guess_lst), self.n_trials - self.count

        self.comment_of_guess = []

        if letter in self.answer:
            positions = [i for i, char in enumerate(self.answer) if char == letter]
            for pos in positions:
                self.guess_lst[pos] = letter
            self.comment_of_guess.append(f"✅ Correct! '{letter}' is in the word.")
        else:
            self.comment_of_guess.append(f"❌ '{letter}' is not in the word.")

        self.count += 1

        if "_" not in self.guess_lst:
            self.finished = True
            return f"🎉 Success! '{self.answer}' is the word!", " ".join(self.guess_lst), self.n_trials - self.count

        if self.count >= self.n_trials:
            self.finished = True
            return f"💀 Out of trials! The word was '{self.answer}'.", " ".join(self.guess_lst), 0

        return "\n".join(self.comment_of_guess), " ".join(self.guess_lst), self.n_trials - self.count


# Gradio interface setup
# Initialize the Hangman game instance
game = Hangman()

# Define Gradio functions
def new_game():
    game.reset_game()
    return game.hint, " ".join(game.guess_lst), game.n_trials, "", ""

def guess(letter):
    result, word_state, trials_left = game.make_guess(letter)
    return '', result, word_state, trials_left, game.hint, "Game Over" if game.finished else ""

# Create Gradio interface
with gr.Blocks() as demo:
    gr.Markdown("## 🎮 Hangman Game ")
    
    with gr.Row():
        new_game_btn = gr.Button("🔄 New Game")
        guess_input = gr.Textbox(label="Enter a Letter", max_lines=1)
    
    with gr.Row():
        word_state = gr.Textbox(label="Word", interactive=False)
        trials_left = gr.Number(label="Trials Left", interactive=False)
    
    with gr.Row():
        hint_display = gr.Textbox(label="Hint", interactive=False)
        game_status = gr.Textbox(label="Status", interactive=False)

    with gr.Row():
        result_output = gr.Textbox(label="Result", interactive=False)
        
    new_game_btn.click(fn=new_game, outputs=[hint_display, word_state, trials_left, result_output, game_status])
    guess_input.submit(fn=guess, inputs=guess_input, outputs=[guess_input, result_output, word_state, trials_left, hint_display, game_status])

# Launch the Gradio app
demo.launch(share=True)
#demo.launch(share=False, server_name="10.87.115.172", server_port=7860)                   # To create a public link, set `share=True` in `launch()`.


# To run this code, ensure you have Gradio installed in your Python environment. You can install it using pip:
# pip install gradio
# Then, run the script, and it will open a local web interface for the Hangman game.
# Enjoy playing!
# End of code