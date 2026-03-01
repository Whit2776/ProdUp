const log_out = async () => {
  let url = '/api/log-out'
  let del = await fetch(url, {method:'GET'})

  if(location.href.includes('staff')){
    location.href = '/dashboard/staff/login/'
    return
  }

  location.href = '/dashboard/auth/login/'
}

document.querySelector('.log-out').addEventListener('click', e => {
  e.preventDefault()
  log_out()
})

try{
  const pop_up_wrapper = document.querySelector('.pop-up-wrapper')
  const add_team_button = document.querySelector('.add-team-button')
  const items = pop_up_wrapper.querySelectorAll('.item')
  Array.from(items).forEach( i => {
    i.onclick = () => {
      pop_up_wrapper.classList.remove('shown')
    }
  })
  add_team_button.addEventListener('click', e => {
    pop_up_wrapper.classList.toggle('shown');
  })
} catch{
  console.log('Add Team Button Not Available on this Page')
}

const get_notification = async () => {
  let url = '/api/get-notification'
  let res = await fetch(url)
  let data = await res.json()
  let notification = data.notification
  
  if (notification){
    document.body.innerHTML += `
      <div class='alert' style='position: fixed; top: 10vh; width: 100%; display:flex; justify-content: center; align-items: center; height: 10vh;'>
        <div style='display: flex; flex-flow: column nowrap; width: max(50%, 250px); background: rgba(31, 212, 203, 0.82); color: white; text-align: center; justify-content: center; align-items: center; padding: 1rem; border-radius: 10px; border: 2px solid rgba(0, 0, 0, 0.1); height: 100%; '>
          <h5 style='margin: 0;'>${notification.title}</h5>
          <p style='margin: 0 overflow: hidden; width: 90%;'>${notification.message}</p
        </div>
      </div>
    `

    setTimeout(()=> {document.querySelector('.alert').remove()}, 3000)
  }

}

setInterval(get_notification, 4000)
