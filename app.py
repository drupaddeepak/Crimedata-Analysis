from flask import Flask, render_template, request
import csv
from flask import Flask
app = Flask(__name__)

# Route for survey form
@app.route('/')
def index():
    return render_template('home.html')

@app.route('/survey')
def survey():
    return render_template('index.html')

# Route to handle form submission
@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        # Get form inputs
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        try:
            # Convert survey responses to integers
            q1 = int(request.form['q1'])  # Mental health rating
            q2 = int(request.form['q2'])  # Stress frequency
            q3 = int(request.form['q3'])  # Sleep hours
            q4 = int(request.form['q4'])  # Self-doubt frequency
            q5 = int(request.form['q5'])  # Awareness of mental health resources
            q6 = int(request.form['q6'])  # Use of mental health services
            q7 = int(request.form['q7'])  # Academic workload effect
            q8 = int(request.form['q8'])  # Happiness level
            q9 = int(request.form['q9'])  # Mindfulness practice
            q10 = int(request.form['q10'])  # Support from friends
            q11 = int(request.form['q11'])  # Comfort discussing mental health
            q12 = int(request.form['q12'])  # Social media impact
            q13 = int(request.form['q13'])  # Time spent on social media
            q14 = int(request.form['q14'])  # Comfort reaching out to professionals
            q15 = int(request.form['q15'])  # Awareness of stress signs
        except ValueError:
            return "Invalid input! Please make sure all questions are answered correctly.", 400

        # Calculate total stress score
        total_stress = q1 + q2 + q3 + q4 + q5 + q6 + q7 + q8 + q9 + q10 + q11 + q12 + q13 + q14 + q15

        # Categorize stress level and provide resources
        stress_level = ""
        extra_content = {}
        
        if total_stress <= 30:
            stress_level = "Low"
            extra_content['spotify'] = "https://open.spotify.com/search/kannada%20lofi/playlists"
        elif 31 <= total_stress <= 60:
            stress_level = "Moderate"
            extra_content['youtube'] = "https://youtu.be/QKBJXjChDHw?si=8RGlZB_FOaGBitEI"
        else:
            stress_level = "High"
            extra_content['doctor'] = {
                "name": "Dr. Vinod Kumar",
                "type": "Consultant Psychiatrist",
                "image": "https://cdn.prod.website-files.com/61d34f30c5a521ccec241100/647dcfe99cecd6060cb012d8_arun.webp",
                "phone": "720483283"
            }

        # Append responses to CSV file
        with open('responses.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                name, age, gender, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, q11, q12, q13, q14, q15,
                total_stress, stress_level
            ])

        # Pass stress information and extra content to submission page
        return render_template(
            'submission.html',
            name=name,
            stress_level=stress_level,
            total_stress=total_stress,
            extra_content=extra_content
        )

if __name__ == '_main_':
    app.run(debug=True)
