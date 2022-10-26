$(document).ready(function(){
	// {% block jquery %}
	// {% endblock %}

	// Contact Form Handler
	var contactForm = $(".contact-form")
	var contactFormMethod = contactForm.attr("method")
	var contactFormEndpoint = contactForm.attr("action")
	

	function displaysubmitting(submitBtn, defaultText, doSubmit){
		if(doSubmit){
			submitBtn.addClass("disabled")
			submitBtn.html("<i class='fa fa-spin fa-spinner'></i> Sending...")
		}else{
			submitBtn.removeClass("disabled")
			submitBtn.html(defaultText)
		}
	}


	contactForm.submit(function(event){
		event.preventDefault()

		var contactFormSubmitbtn = contactForm.find("[type='submit']")
		var contactFormSubmitbtnTxt = contactFormSubmitbtn.text()
		
		var contactFromData = contactForm.serialize()
		var thisForm = $(this)
		displaysubmitting(contactFormSubmitbtn, contactFormSubmitbtnTxt, true)
		$.ajax({
			method: contactFormMethod,
			url: contactFormEndpoint,
			data: contactFromData,
			success: function(data){
				contactForm[0].reset() // clearing out the filled data
				$.alert({
					title: 'Success!',
					content: data.message,
					theme: 'modern',
				})
				setTimeout(function(){
					displaysubmitting(contactFormSubmitbtn, contactFormSubmitbtnTxt, false)
				}, 500)
			},
			error: function(error){
				console.log(error.responseJSON)
				var jsonData = error.responseJSON
				var msg = ""

				$.each(jsonData, function(key, value){ // key, value array index / object
					msg += key + ": " + value[0].message + "<br>"
				})

				$.alert({
					title: 'Opps!',
					content: msg,
					theme: 'modern',
				})

				setTimeout(function(){
					displaysubmitting(contactFormSubmitbtn, contactFormSubmitbtnTxt, false)
				}, 500)
			}
		})
	})



	// Auto Search
	var searchForm = $(".search-form")
	var searchInput = searchForm.find("[name='q']") // input name = 'q'
	var typingTimer;
	var typingInterval = 500 // .5 sec
	var searchBtn = searchForm.find("[type='submit']")

	searchInput.keyup(function(event){
		// key released
		clearTimeout(typingTimer)
		typingTimer = setTimeout(performSearch, typingInterval)
	})

	searchInput.keydown(function(event){
		// key pressed
		clearTimeout(typingTimer)
	})

	function doSearch(){
		searchBtn.addClass("disabled")
		searchBtn.html("<i class='fa fa-spin fa-spinner'></i> Searching...")
	}

	function performSearch(){
		doSearch()
		var query = searchInput.val()
		setTimeout(function(){
			window.location.href = '/search/?q=' + query
		}, 1000)
		
	}


	// Cart + Add Products
	function cartAddRemove(){
		var productForm = $(".form-product-ajax")

		productForm.submit(function(event){
			event.preventDefault();

			var thisForm = $(this)
			var actionEndPoint = thisForm.attr("action")
			var actionEndPoint = thisForm.attr("data-endpoint")
			var httpMethod = thisForm.attr("method")
			var productID = thisForm.find(".cart-item-product-id").attr("value")
			// console.log(productID)
			var formData = thisForm.serialize()

			$.ajax({
				url: actionEndPoint,
				method: httpMethod,
				data: formData,
				success: function(data){
					console.log("success")
					// console.log(data)
					console.log("Added", data.added)
					console.log("Removed", data.removed)
					var submitSpan = thisForm.find(".submit-span")
					if(data.added){
						submitSpan.html('In Cart <button class="btn btn-link">Remove?</button>')
					}else{
						submitSpan.html('<button class="btn btn-success">Add to Cart</button>')
					}

					var navbarCount = $(".navbar-cart-count")
					navbarCount.text(data.cartItemCount)
					var currentPath = window.location.href

					if(currentPath.indexOf("cart") != -1){
						refreshCart()
					}
					console.log("You sure want to delete this item?")
					console.log("parent:")					
					var product = thisForm.parentsUntil(".product-raw")
					console.log(product.val())
					// thisForm.parentsUntil(".product-raw").remove()
					console.log(submitSpan.html())
				},
				error: function(errorData){
					$.alert({
						title: 'Opps!',
						content: 'An error occured',
						theme: 'modern',
					})
				}
			})
		})
	}
	cartAddRemove();
	

	// $(".close").click(function(){
 //    	$("#myAlert").alert("close");
 //    });
 //    $("#myAlert").on('close.bs.alert', function(){
 //        alert('The alert message is about to be closed.');
 //    });


	var cart_delete_item = function(){
		var close = $("#cart_list").find(".close");
		close.attr("data-dismiss", "alert")
		// close.attr("aria-hidden"="true")
		close.alert()

        // var close = $("#cart_list").find(".close");
        // close.on('click', function(){
        //     if (confirm("Do You Really Want to Delete This item ?") === false) {
        //         return false;
        //     }
        // });
    };

	function refreshCart(){
		var cartPrice = $(".cart-price")
		currentUrl = window.location.href
		
		var refreshCartUrl = '/api/cart/'
		var refreshCartMethod = "GET";
		var data = {};
		$.ajax({
			url: refreshCartUrl,
			method: refreshCartMethod,
			data: data,
			success: function(data){
				if(data.products.length > 0){
					cartPrice.find(".cart-subtotal").text(data.subtotal)
					cartPrice.find(".cart-total").text(data.total)
				}else{
					window.location.href = currentUrl
				}
			},
			error: function(errorData){
				$.alert({
					title: 'Opps!',
					content: 'An error occured',
					theme: 'modern',
				})
			}
		})


		// var cartTable = $(".cart-table")
		// var cartBody = cartTable.find(".cart-body")
		// // cartBody.html("<h1>Changed</h1>")
		// var productRows = cartTable.find(".cart-product")
		// currentUrl = window.location.href

		// var refreshCartUrl = '/api/cart/'
		// var refreshCartMethod = "GET";
		// var data = {};
		// $.ajax({
		// 	url: refreshCartUrl,
		// 	method: refreshCartMethod,
		// 	data: data,
		// 	success: function(data){
		// 		console.log("success")
		// 		console.log(data)

				// var hiddenCartItemRemoveForm = $(".cart-item-remove-form")
				// if(data.products.length > 0){
				// 	productRows.html(" ")
				// 	i = data.products.length
				// 	$.each(data.products, function(index, value){
				// 		console.log(value)
				// 		var newCartItemRemove = hiddenCartItemRemoveForm.clone()
				// 		newCartItemRemove.css("display", "block")
				// 		newCartItemRemove.find(".cart-item-product-id").val(value.id)
				// 		cartBody.prepend("<tr><th scope=\"row\">" + i + "</th><td><a href='" + value.url + "'>" + value.name + "</a>" + newCartItemRemove.html() + "</td><td>" + value.price + "</td></tr>")
				// 		i--
				// 	})

				// 	cartBody.find(".cart-subtotal").text(data.subtotal)
				// 	cartBody.find(".cart-total").text(data.total)
				// } else {
				// 	window.location.href = currentUrl
				// }
		// 		cartBody.find(".cart-subtotal").text(data.subtotal)
		// 		cartBody.find(".cart-total").text(data.total)
		// 	},
		// 	error: function(errorData){
		// 		$.alert({
		// 			title: 'Opps!',
		// 			content: 'An error occured',
		// 			theme: 'modern',
		// 		})
		// 	}
		// })					
	}

});