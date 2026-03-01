const team_container = document.getElementById('team_container')

// const pop_up_wrapper = document.querySelector('.pop-up-wrapper')
// const add_team_button = document.querySelector('.add-team-button')

// add_team_button.addEventListener('click', e => {
//   pop_up_wrapper.classList.toggle('active');
// })


const modal = document.getElementById("teamModal");
const openBtn = document.querySelector(".open-add-team-modal-btn");
const closeBtn = document.querySelector(".close-btn");

openBtn.onclick = () => {document.body.style.overflow = 'hidden';modal.classList.add("active")};
closeBtn.onclick = () => {document.body.style.overflow = 'scroll';modal.classList.remove("active")};
window.onclick = (e) => {
if (e.target === modal) modal.classList.remove("active"); document.body.style.overflow = 'scroll';
};

const form = document.getElementById('teamForm')

form.addEventListener('submit',async e => {
  e.preventDefault()
  let url = '/api/create-team'
  let formdata = new FormData(form)
  let data = await fetch(url, {method:'POST', body:formdata})
  let res = await data.json()
  console.log(res)
  append_team(res, team_container)
  modal.classList.remove("active"); document.body.style.overflow = 'scroll'
})

const append_team = (team, team_container) => {
  // Build the team card HTML using JS template literals
  const team_html = `
  <div class="col-lg-4">
    <div class="card">
      <div class="card-body">    
        <div class="row">
          <div class="col-md-6">
            <div class="d-flex align-items-center">
              <div class="flex-shrink-0">
                <img src="/static/dashboard/assets/images/logos/lang-logo/nextjs.png" 
                     alt="" class="thumb-lg rounded-circle"> 
              </div>
              <div class="flex-grow-1 ms-2 text-truncate">
                <h4 class="m-0 fw-semibold text-dark fs-16">${team.name}</h4>   
                <p class="text-dark mb-0 fs-13">Recently : 
                  ${team.availability ? 
                    '<span class="text-success">Available</span>' :
                    '<span class="text-danger">Not Available</span>'}
                </p> 
              </div>
            </div>
          </div>

          <div class="col-md-6 text-end">
            <div class="d-flex align-items-center">
              <div class="flex-grow-1 me-2 text-truncate">
                <h4 class="m-0 fw-semibold text-dark fs-14">${team.leader.name || 'No Leader'}</h4>   
                <p class="text-dark mb-0 fs-13">Team Leader</p> 
              </div>
              <div class="flex-shrink-0">
                <img src="/static/dashboard/assets/images/users/avatar-10.jpg" 
                     alt="" class="thumb-lg rounded-circle"> 
              </div>
            </div>
          </div>
        </div>

        <div class="mt-3">
          <p class="text-muted mb-1 text-t">
            ${team.assigned_project?.[0]?.description || 'No project assigned yet.'}
          </p>
          <p class="text-muted text-end mb-1">${team.progress || 0}% Complete</p>
          <div class="progress mb-3" style="height: 3px;">
            <div class="progress-bar bg-primary" role="progressbar" 
                 style="width: ${team.progress || 0}%;" 
                 aria-valuenow="${team.progress || 0}" aria-valuemin="0" aria-valuemax="100">
            </div>
          </div>
          
          <div class="d-flex justify-content-between">
            <div class="img-group d-flex justify-content-center">
              ${(team.members || []).slice(0, 5).map(member => `
                <a class="user-avatar position-relative d-inline-block ms-n2" href="#">
                  <img src="${member.avatar || '/static/dashboard/assets/images/users/avatar-1.jpg'}" 
                       alt="avatar" class="thumb-md shadow-sm rounded-circle">
                </a>
              `).join('')}
              ${(team.members || []).length > 5 ? `
                <a href="#" class="user-avatar position-relative d-inline-block ms-1">
                  <span class="thumb-md shadow-sm justify-content-center d-flex align-items-center bg-soft-primary rounded-circle fw-semibold fs-6">
                    +${(team.members.length - 5)}
                  </span>
                </a>` : ''}
            </div>

            <div class="align-self-center">
              <button class="btn btn-sm btn-soft-primary">
                <i class="fa-regular fa-message me-1"></i>Message
              </button>
            </div>
          </div>
        </div> 
      </div>
    </div>
  </div>`;

  // Append to DOM
  team_container.innerHTML += team_html;
};
