from flask import Flask, render_template, request, send_file
from io import BytesIO
from xhtml2pdf import pisa

app = Flask(__name__)

questions = [
    {
        "text": "If something were to happen to you, do you feel your life cover would truly secure your family’s future — ideally covering at least 15–20 times your current income?",
        "yes_score": 20, "no_score": 0
    },
    {
        "text": "In case of a medical emergency, are you confident that your health insurance can take care of you and all your loved ones — without causing financial strain?",
        "yes_score": 10, "no_score": 0
    },
    {
        "text": "Do you currently carry any personal or unsecured loans that might weigh down your financial peace of mind?",
        "yes_score": 0, "no_score": 10
    },
    {
        "text": "Do you regularly track where your money goes each month — like following a budget to stay in control?",
        "yes_score": 8, "no_score": 0
    },
    {
        "text": "Have you calculated the corpus needed for you to retire comfortably?",
        "yes_score": 12, "no_score": 0
    },
    {
        "text": "Is your Monthly EMI more than 40% of your monthly take home pay?",
        "yes_score": 0, "no_score": 10
    },
    {
        "text": "Have you ever calculated how much you would need to retire comfortably — so you can stop working without worrying?",
        "yes_score": 10, "no_score": 0
    },
    {
        "text": "Have you done planning for your child’s education and marriage?",
        "yes_score": 10, "no_score": 0
    },
    {
        "text": "In case of any unfortunate event, do you feel your family is financially protected?",
        "yes_score": 10, "no_score": 0
    }
]

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', questions=enumerate(questions))

@app.route('/result', methods=['POST'])
def result():
    doctor_name = request.form.get('doctor_name')
    responses = []
    total_score = 0

    for i, q in enumerate(questions):
        ans = request.form.get(f'q{i}')
        score = q['yes_score'] if ans == 'yes' else q['no_score']
        total_score += score
        responses.append({
            "question": q['text'],
            "answer": ans,
            "score": score,
            "color": "green" if score > 0 else "red"
        })

    return render_template('result.html', responses=responses, total_score=total_score, doctor_name=doctor_name)

@app.route('/download', methods=['POST'])
def download():
    responses = eval(request.form['responses'])
    total_score = int(request.form['total_score'])
    doctor_name = request.form['doctor_name']
    rendered = render_template('result.html', responses=responses, total_score=total_score, doctor_name=doctor_name, download_mode=True)
    
    pdf = BytesIO()
    pisa_status = pisa.CreatePDF(rendered, dest=pdf)
    pdf.seek(0)
    safe_name = doctor_name.replace(" ", "_")
    return send_file(pdf, download_name=f'Dr_{safe_name}_Financial_Assessment.pdf', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
