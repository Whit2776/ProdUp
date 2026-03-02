if(window.innerWidth>600){
  window.addEventListener("scroll", function () {
  const header = document.querySelector(".header");
  const stickyNav = document.querySelector(".header2");

    if (window.scrollY > header.offsetHeight) {
      stickyNav.style.display = "block"; 
      stickyNav.classList.add("active");
    } else {
      stickyNav.style.display = "none";  
      stickyNav.classList.remove("active");
    }
  });
}
const h = document.querySelectorAll('.special_nav_link')
h.forEach( special_nav_link => {
  special_nav_link.addEventListener('click', e => {
    e.preventDefault()
    let parent = special_nav_link.parentElement
    let dropDown = parent.querySelector('.dropdown')
    
    let is_open = dropDown.classList.contains('opened_dropdown')

    h.forEach(j => {
      j.classList.remove('show_dropdown')
      j.parentElement.querySelector('.dropdown').classList.remove('opened_dropdown')
    })

    if(!is_open){
      special_nav_link.classList.add('show_dropdown')
      dropDown.classList.add('opened_dropdown')
    } else {
      special_nav_link.classList.remove('show_dropdown')
      dropDown.classList.remove('opened_dropdown')
    }
  })
})


// Logic to display the navigation panel on mobile devices.
const header = document.querySelector('.header')
const header_2 = document.querySelector('.header2')
const display_buttons = document.querySelectorAll('.menu-icon')
const modal = document.querySelector('.modal')

const openMenu = () => {
  display_buttons.forEach(b => b.classList.add('clicked'))
  header_2.classList.add('is_displayed')
  document.body.classList.add('menu-open');
  modal.classList.add('opened')
  header.classList.add('hidden')
}
const closeMenu = () => {
  display_buttons.forEach(b => b.classList.remove('clicked'))
  header_2.classList.remove('is_displayed')
  document.body.classList.remove('menu-open');
  modal.classList.remove('opened')
  header.classList.remove('hidden')
  h.forEach(j => {
      j.classList.remove('show_dropdown')
      j.parentElement.querySelector('.dropdown').classList.remove('opened_dropdown')
    })
}

display_buttons.forEach(display_button => {
  display_button.onclick = () => {
    if(!display_button.classList.contains('clicked')){
      openMenu()
    } else{
      closeMenu()
    }
  }
})


modal.onclick = () => {
  closeMenu()
}


// --- Swipe Handling ---
let startX = 0;
let endX = 0;

document.addEventListener('touchstart', (e) => {
  startX = e.touches[0].clientX;
  handleSwipe();
});

document.addEventListener('touchend', (e) => {
  endX = e.changedTouches[0].clientX;
  handleSwipe();
});

function handleSwipe() {
  let diff = endX - startX;

  // If nav is open and swipe left (diff < -50)
  if (header_2.classList.contains('is_displayed') && diff < -50) {
    closeMenu()
  }

  // If nav is closed and swipe right from the very left edge
  if (!header_2.classList.contains('is_displayed') && startX < 50 && diff > 50) {
    openMenu()
  }
}
