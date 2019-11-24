/* Project specific Javascript goes here. */


var readyAllFunctions = function() {


	var showSideBar = function() {

		$("header").on("click", "a.item.page-menu", function(event) {

			event.preventDefault();
			event.stopPropagation();

			$sidebar = $("body").find(".ui.left.sidebar.menu");
			$sidebar.sidebar({
				scrollLock: true,
				exclusive: true,
				onHidden: function() {
					$("body").removeClass("pushable");
				}
			}).sidebar("toggle");

		});
		
	};

	var stopDefaultFormSubmit = function($form) {

		if($form === undefined) {

			$(".ui.form").on("submit", function(event) {

				event.preventDefault();
				return false;

			});

		}

		else {

			$form.on("submit", function(event) {
				
				event.preventDefault();
				return false;

			});

		}

	}

	var submitForm = function() {

		$form = $("form.ui.form");
		stopDefaultFormSubmit($form)

		$form.on("click", "input[type=submit]", function(event) {

			var data = $form.serializeArray()
				.filter(function(item){
					if(item.value != "") {
						return item;
					}
				});
			
			var url = $form.attr("action");

			method = 'post'

			if($form.hasClass("sharedSnippet")){

				$modal = $("div.ui.small.modal");

				method = 'get'
				data_uuid = $modal.find("div.uuid-clicked").attr("data-uuid");

				secret_key = $("input[type=text][name=secretKey]").val()

				url = 'show-text/?uuid='+data_uuid+'&&secret_key='+secret_key
			
			}else{
				method = 'post'
			}

			$.ajax({
				method: method,
				url: url,
				data: data
			}).done(function(response) {

				if(response.message){

					$("body")
					.toast({
						class: "error",
						position: "top right",
						message:response.message
					});
				}

				if(response.original_text) {

					$modal.find("div.original-text").html(response.original_text)

					$modal.modal("refresh");

				}else{
					window.location.href = response.redirect;
				}

				
			}).fail(function(xhr, responseJSON) {

				$("body")
				.toast({
					class: "error",
					position: "top right",
					message:xhr.responseJSON.message
				});

				$modal.find("div.ui.small.modal");

				if($modal != undefined){
					$modal.find("div.original_text").html("");
				}
			});
		});


	}

	var showText = function() {

		$(".ui.segment").on("click", "a.show-text", function(event) {

			var dataUUID = $(this).attr("data-uuid");

			console.log("dataUUID = ", dataUUID);

			event.preventDefault();
			event.stopPropagation();

			$modal = $("div.ui.small.modal");

			$modal.modal({
				detachable: false,
				onHide: function () {
					$("input[type=text][name=secretKey]").html("");
				}
			}).modal("show");

			$modal.find("div.uuid-clicked").attr("data-uuid", dataUUID)

		});

	}

	showText();
	submitForm();
	showSideBar();
}



$(document).ready(function() {
	readyAllFunctions();
});
