document.getElementById('diabetes-form').addEventListener('submit', async function(e) {
    e.preventDefault();
    const form = e.target;
    const data = {
        fpg: form.fpg.value,
        hba1c: form.hba1c.value,
        ogtt: form.ogtt.value,
        random_bs: form.random_bs.value,
        symptoms: form.symptoms.value,
        age: form.age.value,
        family_history: form.family_history.value
    };
    
    const response = await fetch('/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });
    const result = await response.json();
    document.getElementById('result').innerHTML = `<div class="result-box"><b>Diagnosis:</b> ${result.diagnosis}<br><b>Recommendation:</b> ${result.recommendation}</div>`;
});
