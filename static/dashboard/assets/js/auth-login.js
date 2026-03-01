const form = document.querySelector('.login-form')
form.addEventListener('submit', async e => {
  e.preventDefault()
  let url = '/api/log-company-in'
  const formdata = new FormData(form)
  const data = await fetch(url, {method:'POST', body: formdata})

  location.href = '/dashboard/'
})