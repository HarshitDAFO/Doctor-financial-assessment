from flask import Flask, render_template, request, send_file
from io import BytesIO
from xhtml2pdf import pisa

app = Flask(__name__)

questions = [
    {
        "text": "Do you have a Life Insurance cover for at least 15 - 20 times of your income?",
        "yes_score": 20, "no_score": 0
    },
    {
        "text": "Do you have health insurance for yourself and all your dependents?",
        "yes_score": 10, "no_score": 0
    },
    {
        "text": "Do you have any personal loans or any unsecured loans?",
        "yes_score": 0, "no_score": 10
    },
    {
        "text": "Do you create a budget for your income?",
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
        "text": "Do you have any Retirement Plan?",
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

    return render_template('result.html', responses=responses, total_score=total_score)

@app.route('/download', methods=['POST'])
def download():
    responses = eval(request.form['responses'])
    total_score = int(request.form['total_score'])

    rendered = render_template('result.html', responses=responses, total_score=total_score, download_mode=True)
    pdf = BytesIO()
    pisa_status = pisa.CreatePDF(rendered, dest=pdf)
    pdf.seek(0)
    return send_file(pdf, download_name='Doctor_Financial_Assessment.pdf', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
