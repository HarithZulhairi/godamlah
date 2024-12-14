// Categories
const categoryList = document.querySelector('.category-list');
const scrollLeftButtonCategories = document.querySelector('#scroll-left-cat');
const scrollRightButtonCategories = document.querySelector('#scroll-right-cat');

// Scroll functionality for Categories
scrollLeftButtonCategories.addEventListener('click', () => {
  categoryList.scrollBy({ left: -300, behavior: 'smooth' });
});

scrollRightButtonCategories.addEventListener('click', () => {
  categoryList.scrollBy({ left: 300, behavior: 'smooth' });
});

// Deals Section
const dealList = document.querySelector('.deal-list');
const scrollLeftButtonDeals = document.querySelector('#scroll-left-deals');
const scrollRightButtonDeals = document.querySelector('#scroll-right-deals');

// Scroll functionality for Deals
scrollLeftButtonDeals.addEventListener('click', () => {
  dealList.scrollBy({ left: -300, behavior: 'smooth' });
});

scrollRightButtonDeals.addEventListener('click', () => {
  dealList.scrollBy({ left: 300, behavior: 'smooth' });
});

// Show/hide buttons for Categories
function updateScrollButtonsCategories() {
  const scrollLeft = categoryList.scrollLeft;
  const scrollWidth = categoryList.scrollWidth - categoryList.clientWidth;

  // Show left button if scrolled right
  if (scrollLeft > 0) {
    scrollLeftButtonCategories.style.display = 'block';
  } else {
    scrollLeftButtonCategories.style.display = 'none';
  }

  // Show right button if there is more content to scroll
  if (scrollLeft < scrollWidth) {
    scrollRightButtonCategories.style.display = 'block';
  } else {
    scrollRightButtonCategories.style.display = 'none';
  }
}

// Show/hide buttons for Deals
function updateScrollButtonsDeals() {
  const scrollLeft = dealList.scrollLeft;
  const scrollWidth = dealList.scrollWidth - dealList.clientWidth;

  // Show left button if scrolled right
  if (scrollLeft > 0) {
    scrollLeftButtonDeals.style.display = 'block';
  } else {
    scrollLeftButtonDeals.style.display = 'none';
  }

  // Show right button if there is more content to scroll
  if (scrollLeft < scrollWidth) {
    scrollRightButtonDeals.style.display = 'block';
  } else {
    scrollRightButtonDeals.style.display = 'none';
  }
}

// Attach event listeners
categoryList.addEventListener('scroll', updateScrollButtonsCategories);
dealList.addEventListener('scroll', updateScrollButtonsDeals);

// Update buttons on load
window.addEventListener('load', () => {
  updateScrollButtonsCategories();
  updateScrollButtonsDeals();
});


// Update buttons on scroll and load
categoryList.addEventListener('scroll', updateScrollButtons);
window.addEventListener('load', updateScrollButtons);


