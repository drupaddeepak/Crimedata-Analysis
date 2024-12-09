from flask import Flask, render_template, request
import csv

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
            q1 = int(request.form['q1'])
            q2 = int(request.form['q2'])
            q3 = int(request.form['q3'])
            q4 = int(request.form['q4'])
            q5 = int(request.form['q5'])
            q6 = int(request.form['q6'])
            q7 = int(request.form['q7'])
            q8 = int(request.form['q8'])
        except ValueError:
            return "Invalid input! Please make sure all questions are answered correctly.", 400

        # Calculate total stress score
        total_stress = q1 + q2 + q3 + q4 + q5 + q6 + q7 + q8

        # Categorize stress level and provide resources
        stress_level = ""
        extra_content = {}
        
        if total_stress <= 16:
            stress_level = "Low"
            extra_content['spotify'] = "https://open.spotify.com/search/kannada%20lofi/playlists"
        elif 17 <= total_stress <= 32:
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
            writer.writerow([name, age, gender, q1, q2, q3, q4, q5, q6, q7, q8, total_stress, stress_level])

        # Pass stress information and extra content to submission page
        return render_template(
            'submission.html',
            name=name,
            stress_level=stress_level,
            total_stress=total_stress,
            extra_content=extra_content
        )

if __name__ == '__main__':
    app.run(debug=True)
