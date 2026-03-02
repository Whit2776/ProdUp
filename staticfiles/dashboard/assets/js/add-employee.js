const form = document.querySelector('.add-employee-form');

form.addEventListener('submit', async e => {
  e.preventDefault();

  const url = '/api/create-employee';
  const formdata = new FormData(form);
  const res = await fetch(url, { method: 'POST', body: formdata });
  const data = await res.json();
  
  if (res.ok) {
    const alert_div = document.createElement('div');
    alert_div.classList.add('floating-alert');
    alert_div.innerHTML = `
      <h2>Employee Created Successfully</h2>
      <p><strong>Name:</strong> ${data.employee.first_name} ${data.employee.last_name}</p>
      <p><strong>Email:</strong> ${data.employee.email}</p>
      <p><strong>Department:</strong> ${data.employee.department}</p>

      <div class="mt-3">
        <p class="text-sm">Temporary Password:</p>
        <code>${data.employee.generated_password}</code>
      </div>
      <small>Make sure to note this password — it won’t be shown again.</small>
      <small>This alert will close in <span class="count-down-15">15</span> seconds ⏳</small>
    `;


    alert_div.style.position = 'fixed';
    alert_div.style.top = '0';
    alert_div.style.left = '50%';
    alert_div.style.transform = 'translateX(-50%)';
    alert_div.style.zIndex = '9999';

    document.body.appendChild(alert_div);

    const countdownSpan = alert_div.querySelector('.count-down-15');
    let timeLeft = 15;

    const interval = setInterval(() => {
      timeLeft--;
      countdownSpan.innerText = timeLeft;
      if (timeLeft <= 0) {
        clearInterval(interval);
        alert_div.remove();
      }
    }, 1000);

    form.reset();
  }
});

// document.getElementById('saveSalary').addEventListener('click', function() {
//   const salary_data = {
//     base_type: document.getElementById('base_type').value,
//     base_rate: document.getElementById('base_rate').value,
//     description: document.getElementById('description').value,
//   };

//   const modal = bootstrap.Modal.getInstance(modalEl);

//   modal.hide();
// });
