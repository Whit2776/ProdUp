const get_employees = async () => {
  let url = '/api/get-employees'
  const res = await fetch(url)
  const employees = await res.json()

  return employees
}



const match_employees_to_carousel = async () => {
  const track = document.querySelector('.carousel-track')
  const employees = await get_employees()
  console.log(employees)

  let EmployeesPerSlide = 6
  let TotalSlides = Math.ceil(employees.length/EmployeesPerSlide)
  // const response = await fetch("https://raw.githubusercontent.com/15Dkatz/official_joke_api/master/jokes/index.json")
  // const jokes = await response.json().slice(0, 101)
  // console.log(jokes)

  for(let i=0;i<TotalSlides;i++){
    let StartingIndex = i*EmployeesPerSlide
    let set = employees.slice(StartingIndex, StartingIndex +EmployeesPerSlide)
    console.log(set)

    let slide = document.createElement('div')
    slide.classList.add('carousel-slide')
    

    set.forEach(s => {
      set_values(slide, s)//, jokes[Math.ceil(Math.random() * jokes.length - 1)])
    })

    track.appendChild(slide)
  }
}

const set_values = (slide, emp, joke) => {
  let employee = document.createElement('div')
    employee.classList.add('employee')
  let img = document.createElement('img')
    img.src = emp.pic_link
  let name = document.createElement('h3')
    name.classList.add('name')
    name.innerText = emp.name
  let func =document.createElement('p')
    func.classList.add('func')
    func.innerText = `${emp.role} | ${emp.department}`
  // let info = document.createElement('p')
  //   info.classList.add('info')
  //   info.innerText = `${joke.setup} ${joke.punchline}`
    
  employee.appendChild(img)
  employee.appendChild(name)
  employee.appendChild(func)
  slide.appendChild(employee)
}

match_employees_to_carousel()