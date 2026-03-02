let chat_link = document.getElementById('chat-link').innerText
let user_id = Number(document.getElementById('id').innerText)
let messages_container = document.querySelector('.messages-container')

let add_files_icon = document.getElementById('add-files-icon')
let add_files_input = document.getElementById('add-files-input')
let preview_container = document.querySelector('.files-preview-container')
let preview = document.querySelector('.files-preview')

let form = document.querySelector('#post-message')
let delete_multiple = document.querySelector('.delete-multiple')

const current_user_mes = document.querySelector('.current-user')
const other_user_mes = document.querySelector('.other-user')

const get_messages = async () => {
  let url = `/chat-api/get-messages/${chat_link}/10`
  let res = await fetch(url)
  let data = await res.json()

  return data
}

const render_messages = async () => {
  let data = await get_messages()
  data.forEach(message => {
    select_element(message, data)
  })

  scrollToBottom()
}

const get_message = async () => {
  let url = `/chat-api/get-message/${chat_link}`
  let res = await fetch(url)
  let data = await res.json()

  if(data.message){
    let messages = Array.from(document.querySelectorAll('.mes'))
    let last = messages[messages.length-1]
    let last_id = Number(last.querySelector('.id').innerText)

    if(last_id === data.id){
      last.querySelector('.state').innerText = data.state
      messages = await get_messages()
      return
    }

    select_element(data, messages)
    scrollToBottom()
  }
}

const post_message = () => {
  let url = `/chat-api/post-message/${chat_link}`

  let send_icon = document.querySelector('.send')
  let submit_btn = document.querySelector('.submit-form')
  send_icon.onclick = () => {
    submit_btn.click()
  }

  form.addEventListener('submit', async e => {
    e.preventDefault()
    let formdata = new FormData(form)
    let res = await fetch(url, {method:'post', body:formdata})
    let data = await res.json()

    let placeHolder = 
      `
        <div id ='' class="d-flex flex-row-reverse current-user mes place-holder" >
          <div class="hidden id"></div>
          <div class="pop-up-wrapper hidden">
            <div class="pop-up">
              <ul class="pop-up-list">
                <li><a href="">Reply</a></li>
                <li><a href="">Edit</a></li>
                <li><a href="">Forward</a></li>
                <li><a href="">Delete</a></li>
              </ul>
            </div>
          </div>
          <img src="{%get_static_prefix%}dashboard/assets/images/users/avatar-3.jpg" alt="user" class="picture rounded-circle thumb-md">
          <div class="me-1 chat-box w-100 reverse">
            <div class="user-chat">
              
              <div class="files-container">
                <div class="files">
                  
                </div>
              </div>
              <p class="message"> </p>
            </div>
            <div class="chat-time date"></div>
            <div class="state">Not Delivered</div>
          </div>
        </div>
      `
    
    if(res.ok){
      form.reset()
      preview.innerHTML = ''
      let messages = await get_messages()
      select_element(data, messages)
      scrollToBottom()
  
      let r = document.querySelector('.reply-preview')
      if(r) document.querySelector('.reply-preview').remove()
      if(location.href.includes('/chat/')) return
      window.parent.moveChatToTop(chat_link)
    }
  })
}



const attach_preview_files = () => {

  add_files_icon.onclick = () => {
    add_files_input.click()
  }

  add_files_input.addEventListener('change', e => {
    let files = Array.from(e.target.files)
    preview_container.classList.toggle('active')
    files.forEach(file => {
      let path = URL.createObjectURL(file)
      let type = file.type

      if(type.includes('image')){
        let div = document.createElement('div')
        let img = document.createElement('img')

        img.src = path
        img.classList.add('fileEl')

        div.classList.add('image-file')
        div.classList.add('file')

        div.appendChild(img)
        preview.appendChild(div)
      }
    })
  })
}


const select_element = (message, messages) => {
  if(message.sender === user_id){
    render_message(messages_container, current_user_mes, message, message.files, messages)
  } else{
    render_message(messages_container, other_user_mes, message, message.files, messages)
  }
}

const scrollToBottom = () => {
  requestAnimationFrame(() => {
    requestAnimationFrame(() => {
      messages_container.scrollTop = messages_container.scrollHeight;
    });
  });
};

window.addEventListener('click', e => {
  if (e.target.classList.contains('modal')) e.target.classList.remove('active')
})

let allow_click_on_mes = false

const render_message = async (container, element, message, files, messages) => {
  //Function used to render messages into the messages container)
  let clone = element.cloneNode(true)
  let messageEl = clone.querySelector('.actual')
  let dateEl = clone.querySelector('.date')
  let files_container = clone.querySelector('.files-container')
  let filesEl = clone.querySelector('.files')
  let pictureEl = clone.querySelector('.picture')
  let idEl = clone.querySelector('.id')
  let stateEl = clone.querySelector('.state')
  if(message.sender === user_id){
    stateEl.innerText = message.state
  }

  if(message.type === 'forward'){
    let span = clone.querySelector('.text-muted')
    span.innerText = 'Forwarded Message'
    span.classList.add('forwarded-message')
  }

  clone.querySelector('.forward-icon').addEventListener('click', e => {
    document.getElementById('forward-message-modal').classList.add('active')
    let input = document.createElement('input')
    input.name = 'message-id'
    input.type = 'hidden'
    input.value = message.id

    document.querySelector('.forward-message-form').appendChild(input)
  })


  messageEl.innerText = message.message
  dateEl.innerText = new Date(message.created).toDateString()
  idEl.innerText = message.id
  //pictureEl.src = user.picture


  if(files != undefined && files.length > 0){
    let i = 0
    
    let m = document.getElementById('view-files-modal')
    let c = m.querySelector('.cards')


    files.forEach(file => {
      if(file.type != null && file.type.includes('image') && i<2){
        let div = document.createElement('div')
        let img = document.createElement('img')

        img.src = file.path
        img.classList.add('file')
        div.appendChild(img)
        filesEl.appendChild(img)
      }

      if(i === 1){
        let g = document.createElement('div')
        g.classList.add('remaining-files')
        g.innerText = `+${files.length-2}`
        filesEl.appendChild(g)
      }
      i++
    })


    filesEl.onclick = () => {
      m.classList.add('active')
      c.innerHTML = ''


      files.forEach(file => {
        let card = document.createElement('div')
        let img1 = document.createElement('img')
        card.classList.add('card')
        img1.src = file.path
        card.appendChild(img1)

        c.appendChild(card)

      })

    }
  }
  clone.querySelector('.reply-icon').onclick = () => {
    reply_message(message, clone, form)
  }

  if(message.type === 'reply'){
    let reply_container = document.createElement('div')
    let replyEL = document.createElement('div')

    let reply_to = messages.find(m => {return m.id === message.reply_to})
    
    reply_container.classList.add('reply-container')
    replyEL.classList.add('reply')

    replyEL.innerText = reply_to.message

    reply_container.appendChild(replyEL)
    clone.querySelector('.user-chat').prepend(reply_container)
  }

  
  longPress(clone, () => {
    allow_click_on_mes = true
    append_to_delete(clone, slide_in_form)
    delete_multiple.parentElement.style.display = 'block'
  })


  container.appendChild(clone)
}


let slide_in_form = document.querySelector('.slide-in-form')

const append_to_delete = (element, form) => {
  let delete_message = document.createElement('div')
  let input = document.createElement('input')
  input.name = 'ids'
  input.type = 'hidden'
  input.value = element.querySelector('.id').innerText
  input.id = `ID${element.querySelector('.id').innerText}`
  input.classList.add('input')

  delete_message.innerText = element.querySelector('.actual').innerText
  delete_message.classList.add(`ID${element.querySelector('.id').innerText}`)
  delete_message.classList.add('delete-message')
  
  if(element.querySelector('.chat-box').classList.contains('selected')){
    element.querySelector('.chat-box').classList.remove('selected')
    slide_in.querySelector(`.ID${element.querySelector('.id').innerText}`).remove()
    form.querySelector(`#ID${element.querySelector('.id').innerText}`).remove()
  } else{
    element.querySelector('.chat-box').classList.add('selected')
    slide_in.querySelector('.delete-messages').appendChild(delete_message)
    form.appendChild(input)
  }
}

slide_in_form.addEventListener('submit', async e => {
  e.preventDefault()
  let url = '/chat-api/delete-message'
  let formdata = new FormData(slide_in_form)
  let res = await fetch(url, {method: 'POST', body:formdata})
  let data = await res.json()

  let delete_messages_container = slide_in.querySelector('.delete-messages')
  let inputs = slide_in_form.querySelectorAll('.input')
  let messages = Array.from(document.querySelectorAll('.mes'))

  if(res.ok){
    delete_multiple.style.display = 'none'
    delete_messages_container.innerHTML = ''
    slide_in.classList.remove('active')
    allow_click_on_mes = false
    inputs.forEach( input => {
      messages.find(mes => {return mes.querySelector('.id').innerText === input.value}).remove()
    })
  }
})

let i = 0

document.addEventListener('click', e => {
  let target = e.target
  if (!target.classList.contains('chat-box')) return
  if (allow_click_on_mes && i > 0){
    append_to_delete(target.parentElement, slide_in_form)
    if(!document.querySelector('.delete-message') ){
      i = -1
      allow_click_on_mes = false
      delete_multiple.parentElement.style.display = 'none'
    }
  }

  i++
})

const reply_message = (message, chat_container, message_form) => {
  try{
    const r = document.querySelector('.reply-preview')
    r.classList.add('disapear')
    setTimeout(() => {r.remove()}, 400)
  } catch (err){
    console.error('Error: ', err)
  }
  let m_t = message_form.querySelector('#message-type')
  let rti = message_form.querySelector('#reply-to-id')
  let reply_preview = document.createElement('div')
  let p = document.createElement('div')
  let c = document.createElement('i')

  c.classList.add('fas')
  c.classList.add('fa-plus')

  m_t.value = 'reply'
  rti.value = message.id

  reply_preview.classList.add('reply-preview')
  reply_preview.appendChild(p)
  reply_preview.appendChild(c)
  form.appendChild(reply_preview)
  p.innerText = `You are replying to: \n ${message.message}`

  c.onclick = () => {
    m_t.value = 'normal'
    reply_preview.classList.add('disapear')
    setTimeout(() => {reply_preview.remove()}, 400)
  }
}

const select_chats = () => {
  let chat_containers = document.querySelectorAll('.chat-container')
  let form = document.querySelector('.forward-message-form')

  Array.from(chat_containers).forEach(cC => {
    cC.onclick = () => {
      let is_selected = cC.classList.contains('selected')
      let chat_input = document.createElement('input')
      let link = cC.querySelector('.link').innerText
      chat_input.classList.add(`a${link}`)
      if(is_selected){
        cC.classList.remove('selected')
        form.querySelector(`.a${link}`).remove()
      } else{
        chat_input.type = 'hidden'
        chat_input.name = 'chat'
        chat_input.value = link
        form.appendChild(chat_input)
        cC.classList.add('selected')
      }

    }
  })
  
  let url = `/chat-api/post-message/${chat_link}`

  form.addEventListener('submit', async e => {
    e.preventDefault()
    let formdata = new FormData(form)
    let res = await fetch(url, {method:'post', body:formdata})
    let data = await res.json()})
}

const search_through =  () => {
  let value = document.querySelector('.search').value
  let chats = document.querySelector('.chats')
  let chats_containers = document.querySelectorAll('.chat-container')

  if(value === ''){
    chats_containers.forEach(chat => {
      chat.style.display = 'flex'
  })
    return
  }
  
  chats_containers.forEach(chat => {
    chat.style.display = 'none'
  })

  
  new_chats = Array.from(chats_containers).filter(chat => {return chat.querySelector('.name').innerText.toLowerCase().includes(value.toLowerCase())})

  new_chats.forEach(c => {
    c.style.display = 'flex'
    chats.prepend(c)
  })

}

document.querySelector('.search').addEventListener('input', e => {
  search_through()
})


let event_is_active = true

function longPress(target, callback, duration = 600) {
  let timer;

  target.addEventListener("mousedown", () => {
    console.log(event_is_active)
    if(!event_is_active) return
    timer = setTimeout(callback, duration);
  });

  target.addEventListener("mouseup", () => {
    clearTimeout(timer);
  });

  target.addEventListener("mouseleave", () => {
    clearTimeout(timer);
  });
}
  

document.addEventListener('DOMContentLoaded', async e => {
  render_messages()
  post_message()
  setInterval(get_message, 4000)
  attach_preview_files()
  select_chats()
})



let is_clicked = false
let slide_in = document.querySelector('.slide-in')
delete_multiple.addEventListener('click', e => {
  slide_in.classList.toggle('active')
  if(is_clicked){
    is_clicked = true
    return
  }
})
