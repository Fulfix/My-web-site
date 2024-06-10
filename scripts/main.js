// Get the toggle button and its container
const themeToggle = document.querySelector('.theme-toggle');
const themeButton = document.querySelector('.theme-button');
const themeIcon = document.querySelector('.theme-icon');

// ...

// Add an event listener to the toggle button
themeButton.addEventListener('click', () => {
  // Toggle the theme
  document.body.classList.toggle('dark-theme');
  document.body.classList.toggle('light-theme');

  themeIcon.src = document.body.classList.contains('dark-theme') ? './images/lune-removebg-preview.png' : '/Users/denis/Thomas/beginner-html-site-styled-gh-pages/images/20240609134543-removebg-preview.png';

  // Update the color of all <p> elements
  const paragraphs = document.querySelectorAll('p');
  paragraphs.forEach((paragraph) => {
    paragraph.style.color = document.body.classList.contains('dark-theme') ? 'black' : 'white';
  });
  const h1 = document.querySelectorAll('h1');
  h1.forEach((h1) => {
    h1.style.color = document.body.classList.contains('dark-theme') ? 'black' : 'white';
  });
  const li = document.querySelectorAll('li');
  li.forEach((li) => {
    li.style.color = document.body.classList.contains('dark-theme') ? 'black' : 'white';
  });
});