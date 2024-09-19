window.addEventListener("scroll",function(){
  var header = document.querySelector("header")
  header.classList.toggle("sticky", window.scrollY > 0)
})

function toggleMobileMenu() {
    document.getElementById("menu").classList.toggle("active");
  }
  

  $('.dropdown-el').click(function(e) {
    e.preventDefault();
    e.stopPropagation();
    $(this).toggleClass('expanded');
    $('#'+$(e.target).attr('for')).prop('checked',true);
  });
  $(document).click(function() {
    $('.dropdown-el').removeClass('expanded');
  });