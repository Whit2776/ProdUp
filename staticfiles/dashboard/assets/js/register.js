const create_company = () => {
  let form = document.querySelector('.company-registeration-form')
  let url = '/api/post-company'

  form.addEventListener('submit', async e => {
    e.preventDefault()

    try {
      const formdata = new FormData(form)
      let data = await fetch(url, {method:'POST', body:formdata})

      if(data.ok){
        alert('Company registered successfully, go to your email to finish set up')
        form.reset()
        
      } else if(data.status === 404){
        location.href = '/dashboard/auth/404/'
      } else if(data.status === 500){
        location.href = '/dashboard/auth/500/'
      } else{
        console.error('Unexpected error', data.status)
      }
    } catch(err){
      console.error('Network Error: ', err)
    }
  })

  compare_passwords(document.querySelector('.password1'),document.querySelector('.password2'), document.getElementById('info')
  )
}

const compare_passwords = (input1, input2, info_div) => {
  //Input 1 is always the first password input
  input2.addEventListener('input', e => {
    if(input2.value === ''){
      info_div.innerHTML = ''
      input2.style.background = 'transparent'
    } else if(input2.value !== input1.value ){
      info_div.innerHTML = `
      <div class="alert alert-danger alert-dismissible fade show shadow-sm border-theme-white-2 mb-0" role="alert">
      <div class="d-inline-flex justify-content-center align-items-center thumb-xs bg-danger rounded-circle mx-auto me-1">
          <i class="fas fa-xmark align-self-center mb-0 text-white "></i>
      </div>
      Passwords do not match.
      
      </div>
      `
      input2.style.background = 'rgba(255, 36, 36, 0.692)'
    } else{
      info_div.innerHTML = ''
      input2.style.background = 'transparent'
    }
  })
}

create_company()
