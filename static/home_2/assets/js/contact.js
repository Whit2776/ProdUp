let form = document.getElementById('contactForm')
form.addEventListener('submit', async e => {
  e.preventDefault()
  const formdata = new FormData(form)

  const res = await fetch('/api/post-message', {method:'POST', body:formdata})
  const message = await res.json()

  if(res.ok){
    form.reset()
    console.log(message)
  } else{
    alert('error')
  }
})