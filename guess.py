from flask import Flask, render_template, request, redirect, url_for, session
import random
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secret key for session management

@app.route('/', methods=["GET", "POST"])
def index():
    # Initialize game session if not already started
    if 'random_number' not in session:
        session['random_number'] = random.randint(1, 100)  # Random number to guess
        session['chances_left'] = 3  # User gets 3 chances
        session['last_guess'] = None  # Initialize last guess
        session['hint'] = ''
        session['message'] = ''
   
    if request.method == 'POST':
        
        num = int(request.form['guess'])  # Get user input
        session['last_guess'] = num  # Store last guess
        return redirect(url_for('game', guess = session['last_guess']))  # Redirect to game logic
        
        
    return render_template('index.html',chances_left=session['chances_left'],  num=session.get('last_guess'),hint = session['hint'],message = session['message'])

@app.route('/game/<int:guess>', methods=["GET", "POST"])
def game(guess):
    
    random_number = session['random_number']
    chances_left = session['chances_left']

    #session['last_guess'] = guess  # Store last guessed number

    if guess == random_number:
        message = "🎉 Congratulations! You won the game!!! 🎉"
        session.pop('random_number')  # Reset game
        session.pop('chances_left')
        session.pop('last_guess')
        return render_template('result.html', message=message)
    else:
        
    # Reduce the number of chances left
        session['chances_left'] -= 1
        chances_left = session['chances_left']

        if chances_left == 0:
            message = f"😢 You lost the game! The correct number was {random_number}"
            session.pop('random_number')
            session.pop('chances_left')
            session.pop('last_guess')
            return render_template('result.html', message=message)

    # Provide hints
        if random_number > 90:
            session['hint'] = "Hint: The number is between 90 and 100"   
        elif random_number < 10:
            session['hint'] = "Hint: The number is between 0 and 10"
        else:
            session['hint']= f"Hint: The number is between {random_number - 10} and {random_number + 10}"

    session['message'] = f"❌ Wrong guess! Try again!"
    return redirect(url_for('index'))
    

if __name__ == '__main__':
    app.run(debug=True)
