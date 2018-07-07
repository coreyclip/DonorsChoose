
$(document).ready(function(){
  "use strict";
  let counter = 0;

	let window_width 	 = $(window).width(),
	window_height 		 = window.innerHeight,
	header_height 		 = $(".default-header").height(),
	header_height_static = $(".site-header.static").outerHeight(),
	fitscreen 			 = window_height - header_height;


	$(".fullscreen").css("height", window_height)
	$(".fitscreen").css("height", fitscreen);

  //-------- Active Sticky Js ----------//
     $(".default-header").sticky({topSpacing:0});

  
  //------- Active Nice Select --------//
     $('select').niceSelect();
     
     
   // -------   Active Mobile Menu-----//

  $(".menu-bar").on('click', function(e){
      e.preventDefault();
      $("nav").toggleClass('hide');
      $("span", this).toggleClass("lnr-menu lnr-cross");
      $(".main-menu").addClass('mobile-menu');
  });


  $('.nav-item a:first').tab('show');



  // Select all links with hashes
  $('.main-menubar a[href*="#"]')
    // Remove links that don't actually link to anything
    .not('[href="#"]')
    .not('[href="#0"]')
    .click(function(event) {
      // On-page links
      if (
        location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') 
        && 
        location.hostname == this.hostname
      ) {
        // Figure out element to scroll to
        let target = $(this.hash);
        target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
        // Does a scroll target exist?
        if (target.length) {
          // Only prevent default if animation is actually gonna happen
          event.preventDefault();
          $('html, body').animate({
            scrollTop: target.offset().top-68
          }, 1000, function() {
            // Callback after animation
            // Must change focus!
            let $target = $(target);
            $target.focus();
            if ($target.is(":focus")) { // Checking if the target was focused
              return false;
            } else {
              $target.attr('tabindex','-1'); // Adding tabindex for elements not focusable
              $target.focus(); // Set focus again
            };
          });
        }
      }
    });

    
 
 });

// -----------LOADING SCREEN - PRELOADER -------------//
$(document).ready(function() {
  //Preloader
  $(window).on("load", function() {
  preloaderFadeOutTime = 1500;
  function hidePreloader() {
  let preloader = $('.spinner-wrapper');
  preloader.fadeOut(preloaderFadeOutTime);
  }
  hidePreloader();
  });
  });


 // --------- ADD ITEMS LIST ON FORM.HTML -------------//

let items  = [];
let prices   = [];
let quantity = [];

let itemInput  = document.getElementById("item");
let priceInput   = document.getElementById("price");
let quantityInput = document.getElementById("quantity");

let priceOutput = document.getElementById("priceform");
let quantityOutput = document.getElementById("quantityform");

let messageBox  = document.getElementById("display");

function insert () {
  items.push(itemInput.value);
  prices.push(priceInput.value);
  quantity.push(quantityInput.value);

clearAndShow();
}

function clearAndShow () {

  // Get the outputs
  // Clear our fields
  itemInput.value = "";
  priceInput.value = "";
  quantityInput.value = "";

  // Show our output
  messageBox.innerHTML = "";

  messageBox.innerHTML += "Items: " + items.join(", ") + "<br/>";
  messageBox.innerHTML += "Prices: " + prices.join(", ") + "<br/>";
  messageBox.innerHTML += "Quantity: " + quantity.join(", ");

  priceOutput.value = prices.join(", ");
  quantityOutput.value = quantity.join(", ");
 }


 //MODAL IMAGES
 // Get the modal
var modal = document.getElementById('myModal');

// Get the image and insert it inside the modal - use its "alt" text as a caption
var img = document.getElementById('myImg');
var modalImg = document.getElementById("img01");
var captionText = document.getElementById("caption");
img.onclick = function(){
    modal.style.display = "block";
    modalImg.src = this.src;
    captionText.innerHTML = this.alt;
}

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks on <span> (x), close the modal
span.onclick = function() { 
  modal.style.display = "none";
}
