const menu_for_phone = document.querySelector('.nav-on-mobile-wrapper')
const open_menu_button = document.querySelector('.open-menu')
const close_menu_button = document.querySelector('.close-menu')


open_menu_button.onclick = () => {
  menu_for_phone.classList.remove('hidden')
  document.querySelector('.on-mobile').style.left = 0;
}

menu_for_phone.onclick = () => {
  menu_for_phone.classList.add('hidden')
  document.querySelector('.on-mobile').style.left = '-1000px';

}

close_menu_button.onclick = () => {
  menu_for_phone.classList.add('hidden')
  document.querySelector('.on-mobile').style.left = '-1000px';
}
