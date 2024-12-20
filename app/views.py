from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session, Response # Message handling, page switching.
import re
import json
from verbecc import Conjugator

views = Blueprint('user', __name__)

def checkAuth():
    if "id" in session:
        current_user = session['email']
        return(current_user)
    else:
        return Response(response="Unauthorized", status=401)

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


@views.route('/dashboard', methods=["GET", "POST"])
def display_statistics():
    user_email = checkAuth()


    return render_template("dashboard.html", user_email=user_email)

@views.route('/begin_exercise', methods=["GET", "POST"])
def customise_exercise():
    checkAuth()
    er_verbs = []
    re_verbs = []
    ir_verbs = []

    with open(r"C:\Users\danie\OneDrive\Desktop\Conjugator\app\static\verbs.json", "r", encoding="utf-8") as file:
        verbs = json.load(file) # load() expects a file, loads() expects a string

    for verb in verbs: # Iterates through the verbs in the JSON file
        if verb["verb"][-4:] == "er": # Checks if the verb ends with "er", then "re", then "ir"
            er_verbs.append(verb["verb"])
        elif verb["verb"][-4:] == "re":
            re_verbs.append(verb["verb"])
        elif verb["verb"][-4:] == "ir":
            ir_verbs.append(verb["verb"])

    return render_template("customiseExercise.html", er_verbs=er_verbs, re_verbs=re_verbs, ir_verbs=ir_verbs)

@views.route('/logout')
def logout():
    session.clear() # Removes all details from the current session.
    flash("Logged out successfully.")
    return redirect(url_for("auth.authenticate")) # Redirects to login page