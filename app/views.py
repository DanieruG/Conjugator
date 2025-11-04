from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session, Response # Message handling, page switching.
import re
import json
from verbecc import Conjugator
from .DSA import LinkedList, Node
from .models import Users, Exercises
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from . import db
from werkzeug.security import generate_password_hash, check_password_hash


views = Blueprint('user', __name__)

lst = LinkedList()

### USED FOR GENERATING VERBS JSON FILE ###

# verb_pairs = []
# # Do not forget to account for reflexive verbs later on.

# with open(r"C:\Users\danie\OneDrive\Desktop\Conjugator\app\static\french_verbs.txt", "r", encoding="utf-8") as verb_file:
#     # Encoding adjusted to recognise special characters.
#     for line in verb_file:
#         broken_text = re.split(r"\s+", line, maxsplit=1) # "\s+" deals with whitespace characters
#         broken_text[1] = broken_text[1].lstrip() # Removes leading whitespace.
#         broken_text[1] = broken_text[1].rstrip() # Removes /n new line
#         verb_pairs.append(tuple(broken_text))

# verb_dict = [{"verb": verb, "translation": translation} for verb, translation in verb_pairs]
# # Dictionary comprehension to create dictionary where verb is stored alongside translation.

# with open(r"C:\Users\danie\OneDrive\Desktop\Conjugator\app\static\verbs.json", "w", encoding="utf-8") as file:
#     json.dump(verb_dict, file, indent=4, ensure_ascii=False)
#     # Indent maintains readablity, ensure_ascii ensures that accented characters are represented correctly.

# print("JSON Created.")

# cg = Conjugator(lang='fr')
# print(cg.conjugate("manger"))
# manger_conjug = cg.conjugate("manger")

# print(manger_conjug['moods']['indicatif']["présent"]) # This is how to access tenses.

# forbidden_verbs = ["pleuvoir", "falloir", "neiger", "grêler", "tonner", "s'agir", "choir", "clore", "seoir", "ouïr", "gésir", "échoir"]

pronoun_dict = {
    "Je": 0,
    "Tu": 1,
    "Il/Elle/On": 2,
    "Nous": 3,
    "Vous": 4,
    "Ils/Elles": 5
}

class questionRecord:
    def __init__(self, question_id, conjugated_verb, infinitive, tense, pronoun):
        self.question_id = question_id # Unique identifier for each question. A hash.
        self.conjugated_verb = conjugated_verb # The answer
        self.infinitive = infinitive # The infinitive form of the verb
        self.tense = tense # The tense of the verb; will be a mood tense pair.
        self.pronoun = pronoun
        self.validate = False # User's answer is either True or False.

    def validate_answer(self, user_answer):
        if user_answer.lower() == self.conjugated_verb.lower():
            self.validate = True
            return self.validate
        else:
            self.validate = False
            return self.validate

    
    def get_question_id(self):
        return self.question_id
    
    def get_conjugated_verb(self):
        return self.conjugated_verb
    
    def get_infinitive(self):
        return self.infinitive
    
    def get_tense(self):
        return self.tense

    def get_pronoun(self):
        return self.pronoun


def translation_check(verb): # This searches for the translation of the verb
    with open(r"app\static\verbs.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    for item in data:
        if item.get("verb") == verb:
            return item.get("translation")
    
    return "Translation was not found."


@views.route('/dashboard', methods=["GET", "POST"])
def showDashboard():
    try:
        user_email = session['email']
    except KeyError:
        return Response(response="Unauthorized", status=401)

    return render_template("dashboard.html", user_email=user_email)

exercise_details = None
@views.route('/fetch_details', methods=["GET"])
def display_statistics(): # To display the statistics of the user.
    exercises = Exercises.query.filter_by(id=session['id']).all() # Gets all exercises for the user.

    if not exercises: # If no exercises are found, this subroutine should be skipped.
        return
    
    num_exercises = Exercises.query.filter_by(id=session['id']).count() # Counts the number of exercises.

    best_exercise = Exercises.query.order_by(Exercises.correct.desc()).first() # Fetches the ID of the best exercise.
    
    worst_exercise = Exercises.query.order_by(Exercises.incorrect.desc()).first() # Fetches the ID of the worst exercise.

    print(worst_exercise.exercise_id)

    total_correct = 0
    total_incorrect = 0
    total_time = 0
    total_questions = 0

    for exercise in exercises: # Loops through each record, and fetches the details.
        total_correct = total_correct + exercise.correct
        total_incorrect = total_incorrect + exercise.incorrect
        total_time = total_time + exercise.timeElapsed
        total_questions = total_questions + exercise.totalQuestions # Sums up the total number of questions.
    
    rateCorrect = (total_correct / total_questions) * 100
    rateIncorrect = (total_incorrect / total_questions) * 100
    
    response = { 
        "leftTable": {
        "exerciseCount": num_exercises,
        "totalCorrect": total_correct,
        "totalIncorrect": total_incorrect,
        "totalTime": total_time,
        "totalQuestions": total_questions,
        "rateCorrect": rateCorrect,
        "rateIncorrect": rateIncorrect,
        "worstExercise": "Exercise " + str(worst_exercise.exercise_id),
        "bestExercise": "Exercise " + str(best_exercise.exercise_id)
    },
    }

    exercise_history = { # This stores the user's exercise history.
        "rightTable": {
            f"Exercise {record.exercise_id}": {
                "question_data": record.question_data,
                "correct": record.correct,
                "incorrect": record.incorrect,
                "total_time": record.timeElapsed,
                "timestamp": record.timestamp.strftime("%d/%m/%Y %H:%M")
            }
            for i, record in enumerate(exercises)  # Loop through fetched records
        }
    }

    response.update(exercise_history) # Combines the two dictionaries.
        
    
    return jsonify(response)


@views.route('/begin_exercise', methods=["GET", "POST"])
def customise_exercise():
    global exercise_details
    try:
        user_email = session['email']
    except KeyError:
        return Response(response="Unauthorized", status=401)
    
    er_verbs, re_verbs, ir_verbs = options_loader()

    if request.method == "POST":
        data = request.get_json() # Treat as a dictionary.

        selected_verbs = data["selected_verbs"]
        selected_tenses = data["selected_tenses"] # also treated as a dictionary
        selected_pronouns = data["selected_pronouns"]
        session["duration"] = data["duration"]
        exercise_details = exercise_generator(selected_verbs, selected_tenses, selected_pronouns)
    
        return jsonify({"success":"Details received successfully."}), 200
    
    return render_template("customiseExercise.html", er_verbs=er_verbs, re_verbs=re_verbs, ir_verbs=ir_verbs)


def options_loader():
    er_verbs = []
    re_verbs = []
    ir_verbs = []

    with open(r"C:\Users\danie\OneDrive\Desktop\Conjugator\app\static\verbs.json", "r", encoding="utf-8") as file:
        verbs = json.load(file) # load() expects a file, loads() expects a string

    for verb in verbs: # Iterates through the verbs in the JSON file
        if verb["verb"].endswith("er"): # Checks if the verb ends with "er", then "re", then "ir"
            er_verbs.append(verb["verb"])
        elif verb["verb"].endswith("re"):
            re_verbs.append(verb["verb"])
        elif verb["verb"].endswith("ir"):
            ir_verbs.append(verb["verb"])


    return er_verbs, re_verbs, ir_verbs

def exercise_generator(selected_verbs, selected_tenses, selected_pronouns):
    questions = LinkedList()
    cg = Conjugator(lang='fr')
    # one question each for a pronoun, tense, and verb.
    for verb in selected_verbs: # Iterates through the selected verbs
        for mood in selected_tenses:
            if selected_tenses[mood]: # If the mood is selected, so the list attached to they key is not empty.
                tense_list = selected_tenses[mood] # List of tenses for the mood.
                for pronoun in selected_pronouns:
                    for tense in tense_list:
                        raw_conjugations = cg.conjugate(verb)
                        conjugation = raw_conjugations['moods'][mood][tense][pronoun_dict[pronoun]]
                        new_question = questionRecord(hash(pronoun + verb + mood + tense), conjugation, verb, (mood, tense), pronoun) # mood tense as a tuple.
                        questions.AddToStart(new_question)
    return questions



# Get the linked list.
# Get the head element.
# Button action; next node, path.
# Its all different routes


@views.route('/main_exercise', methods=["GET", "POST"])
def load_exercise():
    try:
        user_email = session['email']
    except KeyError:
        return Response(response="Unauthorized", status=401)
    
    return render_template("exercise.html")

@views.route('/initialise', methods=["GET"])
def index():
    global exercise_details

    question = exercise_details.getHead()
    mood_tense = question.get_tense()
    translation = translation_check(question.get_infinitive())
    question_count = exercise_details.size()

    return jsonify({ # Sends a JSON object to JS side
        "mood":f"{mood_tense[0]}",
        "tense":f"{mood_tense[1]}",
        "infinitive":f"{question.get_infinitive()}",
        "pronoun":f"{question.get_pronoun()}",
        "translation": f"{translation}",
        "count": f"{question_count}",
        "duration": f"{session['duration']}"
    })   

@views.route('/next', methods=["GET", "POST"])
def next_question():
    global exercise_details
    
    question = exercise_details.next()
    if question is None:
        return "You have reached the end of the exercise!", 400

    mood_tense = question.get_tense() # 08/02/2025 16:19, this line keeps getting triggered despite the try except block.
    translation = translation_check(question.get_infinitive())

    return jsonify({ # Sends a JSON object to JS side
        "mood":f"{mood_tense[0]}",
        "tense":f"{mood_tense[1]}",
        "infinitive":f"{question.get_infinitive()}",
        "pronoun":f"{question.get_pronoun()}",
        "translation": f"{translation}"
    }) 


@views.route('/previous', methods=["GET"])
def prev_question():
    global exercise_details

    question = exercise_details.prev()
    if question is None:
        return "You have reached the end of the exercise!", 400

    mood_tense = question.get_tense()
    translation = translation_check(question.get_infinitive())

    return jsonify({ # Sends a JSON object to JS side
        "mood":f"{mood_tense[0]}",
        "tense":f"{mood_tense[1]}",
        "infinitive":f"{question.get_infinitive()}",
        "pronoun":f"{question.get_pronoun()}",
        "translation": f"{translation}"
    })   

@views.route('/marking', methods=["POST", "GET"])
def mark():
    global exercise_details

    if request.method == "POST":
        data = request.get_json()
        q_count = exercise_details.size()
        correct = 0 # Count of correct answers
        wrong = 0 # Count of wrong answers
        count = 1 # Counter for the questions
        packaged_details = []

        current_q = exercise_details.getHead()
        while count != q_count + 1: # While the count is not equal to the question count
            result = current_q.validate_answer(data[f"{count}"]) # Validate the answer
            if result: # If the answer is correct
                correct = correct + 1
                result = "Correct"
            else:
                wrong = wrong + 1
                result = "Incorrect"
            
            tense_mood = current_q.get_tense() # Get the tense and mood of the question
            pckg = (data[f"{count}"], current_q.get_conjugated_verb(), current_q.get_infinitive() + " - " + tense_mood[0] + ", " + tense_mood[1] + " tense" + " - " + current_q.get_pronoun(), result)
            packaged_details.append(pckg)
            # Tuple created with user's answer, actual answer, and the question.
            try:
                current_q = exercise_details.next() # Move to the next question, unless it is the last question.
            except AttributeError:
                break # Breaks the loop if it is the last question.
            count = count + 1 # Increment the counter.
        
        print(data)
        response = { # This creates a dictionary using iteration. For each element, the question number is incremented.
                    str(i+1): {
                        "user_ans": user_ans,
                        "answer": answer,
                        "question": question,
                        "result": result
                    }
                    for i, (user_ans, answer, question, result) in enumerate(packaged_details)
                }
        
        minutes_elapsed = data["minutes"]
        seconds_elapsed = data["seconds"]

        add_details = {
            "details": { # This is working fine.
            "correct": correct,
            "wrong": wrong,
            "total": q_count,
            "minutes": minutes_elapsed,
            "seconds": seconds_elapsed
        }}
        
        response.update(add_details) # Response now contains everything.
        
        storeExercise(response, add_details) # Pushes the data to the database.

        session['exercise_summary'] = response # Stores exercise summary data within the session.

        return jsonify(response)
    
    return Response(response="Unauthorized", status=401), 400 # Test response in case POST method is not used.

    # Details required on the front-end
    # Question count
    # Number you got wrong, number you got right
    # for each question:
    # question number, question, user's answer, actual answer.

def storeExercise(response, add_details):
    success = False
    response = json.dumps(response, ensure_ascii=False)

    new_exercise = Exercises(
        id=session['id'], 
        question_data=response, 
        correct=add_details["details"]["correct"], 
        incorrect=add_details["details"]["wrong"], 
        totalQuestions=add_details["details"]["total"], 
        timeElapsed=add_details["details"]["minutes"]*60 + add_details["details"]["seconds"]
        )
    
    try:
        db.session.add(new_exercise) # Adds a exercise to the database
        db.session.commit() # Saves this change
        success = True
    except Exception as e: # If for whatever reason this fails, any changes are undone.
        db.session.rollback() # Undoes changes
        print(e)
        success = False
    
    if success:
        print(success)
        return "The details have been added into the database successfully.", 200

    print(success)
    return "The details could not be added into the database.", 400




@views.route('/exercise_summary', methods=["POST", "GET"])
def load_summary():
    try:
        user_email = session['email']
    except KeyError:
        return Response(response="Unauthorized", status=401)
    
    return render_template("summary.html")

@views.route('/summary', methods=["GET"])
def summary():
    data = session['exercise_summary']
    if data:
        return jsonify(session['exercise_summary'])

    return Response(response="No data found.", status=404)

@views.route('/exercise_recall', methods=["GET"])
def load_resummary():
    try:
        user_email = session['email']
    except KeyError:
        return Response(response="Unauthorized", status=401)
    
    return render_template("reSummary.html")

@views.route('/settings', methods=["GET", "POST"])
def load_settings():
    try:
        user_email = session['email']
    except KeyError:
        return Response(response="Unauthorized", status=401)
    
    return render_template("settings.html")

@views.route('/update_details', methods=["POST"])
def update_details():
    data = request.get_json()
    user = Users.query.filter_by(id=session['id']).first()
    currentPassword = data["currentPasswordField"]
    print(currentPassword)

    emailChange = False
    passChange = False

    messages = {
        "emailStatus": "Your email was not changed.",
        "passwordStatus": "Your password was not changed"
    }

    if check_password_hash(user.password, currentPassword):
        # Attempting to update the password.
        try:
            newPassword = data["newPasswordField"]
            hashedPassword = generate_password_hash(newPassword)
            user.password = hashedPassword
            db.session.commit()

            passChange = True
        except Exception as e:
            print(e)
            db.session.rollback()

        # Attempting to update the email
        try:
            newEmail = data["emailField"]
            user.email = newEmail
            db.session.commit()
            emailChange = True

        except Exception as e:
            print(e)
            db.session.rollback()
    else:
        print(f"Data should be here: {data} ")
        return jsonify({"message": "Wrong password entered for confirmation."}), 401


    if emailChange:
        messages["emailStatus"] = "Your email has been changed."

    if passChange:
         messages["passwordStatus"] = "Your password has been changed."
        
    return jsonify(messages), 200



@views.route('/logout')
def logout():
    session.clear() # Removes all details from the current session.
    flash("Logged out successfully.")
    return redirect(url_for("auth.authenticate")) # Redirects to login page