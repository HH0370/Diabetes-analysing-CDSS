from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


# Diabetes diagnosis function based on WHO/ADA diagnostic criteria
def analyze_diabetes(data):
    age = int(data.get('age', 0)) if data.get('age') else 0
    family_history = data.get('family_history', 'no')
    
    # Check each criterion if provided
    diabetic_criteria = []
    pre_diabetic_criteria = []
    
    # Criterion 1: Fasting Plasma Glucose (FPG) >= 126 mg/dL
    fpg = data.get('fpg', '').strip()
    if fpg:
        fpg_val = float(fpg)
        if fpg_val >= 126:
            diabetic_criteria.append('FPG')
        elif fpg_val >= 100:
            pre_diabetic_criteria.append('FPG')
    
    # Criterion 2: HbA1c >= 6.5%
    hba1c = data.get('hba1c', '').strip()
    if hba1c:
        hba1c_val = float(hba1c)
        if hba1c_val >= 6.5:
            diabetic_criteria.append('HbA1c')
        elif hba1c_val >= 5.7:
            pre_diabetic_criteria.append('HbA1c')
    
    # Criterion 3: Oral Glucose Tolerance Test (OGTT - 2 hour) >= 200 mg/dL
    ogtt = data.get('ogtt', '').strip()
    if ogtt:
        ogtt_val = float(ogtt)
        if ogtt_val >= 200:
            diabetic_criteria.append('OGTT')
        elif ogtt_val >= 140:
            pre_diabetic_criteria.append('OGTT')
    
    # Criterion 4: Random Blood Sugar >= 200 mg/dL with symptoms
    random_bs = data.get('random_bs', '').strip()
    symptoms = data.get('symptoms', 'no')
    if random_bs:
        random_val = float(random_bs)
        if random_val >= 200 and symptoms == 'yes':
            diabetic_criteria.append('Random BS with symptoms')
        elif random_val >= 200:
            diabetic_criteria.append('Random BS (confirm with symptoms)')
    
    # Determine diagnosis
    if diabetic_criteria:
        criteria_str = ', '.join(diabetic_criteria)
        return {
            'diagnosis': 'DIABETIC',
            'recommendation': f'You meet the diagnostic criteria for diabetes based on: {criteria_str}. Consult a doctor immediately for confirmation and treatment plan.'
        }
    elif pre_diabetic_criteria:
        criteria_str = ', '.join(pre_diabetic_criteria)
        return {
            'diagnosis': 'PRE-DIABETIC',
            'recommendation': f'Pre-diabetes detected based on: {criteria_str}. Implement lifestyle changes and regular monitoring.'
        }
    elif any([fpg, hba1c, ogtt, random_bs]):
        return {
            'diagnosis': 'NON-DIABETIC',
            'recommendation': 'Based on the provided test results, you do not meet the diagnostic criteria for diabetes. Maintain healthy lifestyle practices.'
        }
    else:
        return {
            'diagnosis': 'INCOMPLETE DATA',
            'recommendation': 'Please enter at least one test result for analysis.'
        }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    data = request.form.to_dict()
    result_data = analyze_diabetes(data)
    return render_template('result.html', diagnosis=result_data['diagnosis'], recommendation=result_data['recommendation'])

if __name__ == '__main__':
    app.run(debug=True)
