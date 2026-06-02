import sqlite3

from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/assessment')
def assessment():
    return render_template('assessment.html')

@app.route('/questionnaire')
def questionnaire():
    return render_template('questionnaire.html')

@app.route('/history')
def history():

    conn = sqlite3.connect('wellness.db')

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM assessments")

    records = cursor.fetchall()

    conn.close()

    return render_template(
        'history.html',
        records=records
    )


@app.route('/analyze', methods=['POST'])
def analyze():

    # -------------------------
    # Initialize Scores
    # -------------------------

    vata = 0
    pitta = 0
    kapha = 0
    wellness = 100

    # -------------------------
    # Get Form Data
    # -------------------------

    answers = {}

    for key in request.form:
        answers[key] = int(request.form[key])

    # -------------------------
    # VATA CALCULATION
    # -------------------------

    vata += answers['p1'] * 3
    vata += answers['p2'] * 3
    vata += answers['p3'] * 3
    vata += answers['p5'] * 2
    vata += answers['p7'] * 2
    vata += answers['p9'] * 3

    vata += answers['v11'] * 3
    vata += answers['v13'] * 3
    vata += answers['v14'] * 3
    vata += answers['v17'] * 2
    vata += answers['v19'] * 2

    vata += answers['n29'] * 2
    vata += answers['n30'] * 3


    # -------------------------
    # PITTA CALCULATION
    # -------------------------

    pitta += answers['p4'] * 3
    pitta += answers['p6'] * 3
    pitta += answers['p8'] * 3

    pitta += answers['v15'] * 3
    pitta += answers['v16'] * 3
    pitta += answers['v18'] * 3

    pitta += answers['n22'] * 1
    pitta += answers['n27'] * 2
    pitta += answers['n28'] * 1


    # -------------------------
    # KAPHA CALCULATION
    # -------------------------

    kapha += answers['p10'] * 3

    kapha += answers['v12'] * 3
    kapha += answers['v20'] * 3
    kapha += answers['v19'] * 1

    kapha += answers['n23'] * 2
    kapha += answers['n24'] * 3
    kapha += answers['n25'] * 1
    kapha += answers['n26'] * 1
    kapha += answers['n27'] * 1
    kapha += answers['n28'] * 1


    # -------------------------
    # WELLNESS SCORE
    # -------------------------

    wellness -= answers['v11']
    wellness -= answers['v12']
    wellness -= answers['v13']
    wellness -= answers['v14']
    wellness -= answers['v15']
    wellness -= answers['v16']
    wellness -= answers['v17']
    wellness -= answers['v18']
    wellness -= answers['v19']
    wellness -= answers['v20']

    wellness -= answers['n21'] * 3
    wellness -= answers['n22'] * 2
    wellness -= answers['n23'] * 3
    wellness -= answers['n24'] * 3
    wellness -= answers['n25'] * 2
    wellness -= answers['n26'] * 2
    wellness -= answers['n27'] * 3
    wellness -= answers['n28'] * 3
    wellness -= answers['n29'] * 2
    wellness -= answers['n30'] * 2

    if wellness < 0:
        wellness = 0


    # -------------------------
    # FIND DOMINANT DOSHA
    # -------------------------

    doshas = {
        "Vata": vata,
        "Pitta": pitta,
        "Kapha": kapha
    }

    dominant_dosha = max(doshas, key=doshas.get)
    
    conn = sqlite3.connect('wellness.db')

    cursor = conn.cursor()

    cursor.execute("""
                   INSERT INTO assessments
                   (name, age, gender, vata, pitta, kapha,
                    wellness, dominant_dosha)

                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    ( 
                        request.form.get("name"),
                        request.form.get("age"),
                        request.form.get("gender"),
                        vata,
                        pitta,
                        kapha,
                        wellness,
                        dominant_dosha
                    ))

    conn.commit()
    conn.close()


    # -------------------------
    # RECOMMENDATIONS
    # -------------------------

    if dominant_dosha == "Vata":
        recommendation = """
        Warm cooked foods,
        regular sleep schedule,
        meditation,
        oil massage,
        grounding activities.
        """

    elif dominant_dosha == "Pitta":
        recommendation = """
        Cooling foods,
        avoid excessive spicy meals,
        mindfulness practices,
        adequate hydration,
        stress management.
        """

    else:
        recommendation = """
        Regular exercise,
        lighter meals,
        morning sunlight exposure,
        active lifestyle,
        reduced sedentary habits.
        """


    return render_template(
        'dashboard.html',
        vata=vata,
        pitta=pitta,
        kapha=kapha,
        wellness=wellness,
        dominant_dosha=dominant_dosha,
        recommendation=recommendation
    )

if __name__ == '__main__':
    app.run(debug=True) 