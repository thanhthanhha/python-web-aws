/*
	Strata by HTML5 UP
	html5up.net | @ajlkn
	Free for personal and commercial use under the CCA 3.0 license (html5up.net/license)
*/

(function($) {

	var $window = $(window),
		$body = $('body'),
		$header = $('#header'),
		$menu = $('#menu'),
		$footer = $('#footer'),
		$sidebar = $('#sidebar'),
		$main = $('#main'),
		settings = {

			// Parallax background effect?
				parallax: true,

			// Parallax factor (lower = more intense, higher = less intense).
				parallaxFactor: 20

		};
	// Touch?
		if (browser.mobile) {

			// Turn on touch mode.
				$body.addClass('is-touch');

			// Height fix (mostly for iOS).
				window.setTimeout(function() {
					$window.scrollTop($window.scrollTop() + 1);
				}, 0);

		}

	// Footer.
		breakpoints.on('<=medium', function() {
			$footer.insertAfter($main);
		});

		breakpoints.on('>medium', function() {
			$footer.appendTo($header);
		});

	// Main Sections: Two.

		// Lightbox gallery.
			$window.on('load', function() {

				$('#two').poptrox({
					caption: function($a) { return $a.parent().next('h3').text(); },
					overlayColor: '#2c2c2c',
					overlayOpacity: 0.85,
					popupCloserText: '',
					popupLoaderText: '',
					selector: '.work-item a.image',
					usePopupCaption: true,
					usePopupDefaultStyling: false,
					usePopupEasyClose: false,
					usePopupNav: true,
					windowMargin: (breakpoints.active('<=small') ? 0 : 50)
				});

			});

		//change Profile Picture when upload
		$('#id_image').on('change', function() {
			var input = $(this)[0];
			console.log("function working")
			if (input.files && input.files[0]) {
				console.log("in condition")
				var reader = new FileReader();
				reader.onload = function(e) {
				$('#profile-picture').attr('src', e.target.result);
				}
				reader.readAsDataURL(input.files[0]);
      		}
		});

		// Search (header).
		var $search = $('#search'),
			$search_input = $search.find('input');

		$body
			.on('click', '[href="#search"]', function(event) {

				event.preventDefault();

				// Not visible?
					if (!$search.hasClass('visible')) {

						// Reset form.
							$search[0].reset();

						// Show.
							$search.addClass('visible');

						// Focus input.
							$search_input.focus();

					}

			});

		$search_input
			.on('keydown', function(event) {

				if (event.keyCode == 27)
					$search_input.blur();

			})
			.on('blur', function() {
				window.setTimeout(function() {
					$search.removeClass('visible');
				}, 100);
			});

	// Intro.
		var $intro = $('#intro');

		// Move to main on <=large, back to sidebar on >large.
			breakpoints.on('<=large', function() {
				$intro.prependTo($main);
			});

			breakpoints.on('>large', function() {
				$intro.prependTo($sidebar);
			});

	//toggle Edit

	$(document).ready(function() {
		//control post update send API
		$('.dropdown-menu .dropdown-item[data-toggle="modal"]').click(function() {
		  var postElement = $(this).closest('.work-item');
		  var postPK = postElement.data('post-pk');
		  var form = $('#form-update');

		  var host = window.location.host;
		  var actionURL = '//' + host + '/blog/post/edit/' + postPK + '/';
		  form.attr('action', actionURL);

		  var title = postElement.find('h3').text();
		  var content = postElement.find('p').text();
	  
		  $('#form-update #id_title').val(title);
		  $('#form-update #id_content').val(content);
		});

		//delete post handler
		$('.delete-btn').on('click', function() {
			var postElement = $(this).closest('.work-item');
		  	var postPK = postElement.data('post-pk');
			var host = window.location.host;
			var deleteUrl = '//' + host + '/blog/post/delete/' + postPK + '/';
			var token = $(this).data('token');
			
			console.log(`working ${deleteUrl}`);

			$.ajax({
				url: deleteUrl,
				type: 'POST',
				data: {
					csrfmiddlewaretoken: token
				},  
				success: function(response) {
					console.log('Post deleted successfully');
					location.reload()
				},
				error: function(xhr, status, error) {
					console.log('Error deleting post:', error);
				}
			});
		});	
	  });

	  //like post handler
	    $('.like-button').on('click', function() {
            
            var host = window.location.host;
            var postElement = $(this).closest('.work-item');
			if (postElement.length <= 0) {
				postElement = $(this).closest('.reply-section');
			}
		  	var postPK = postElement.data('post-pk');
			console.log(postPK)
			var commented = postElement.hasClass('reply-section');
			var likeUrl = '//' + host + '/blog/post/like/';
			var signinURL = '//' + host + '/profile/signin/';
			var token = $(this).parent().data('token');

            $.ajax({
                type: 'POST',
                url: likeUrl,
                data: {
                    csrfmiddlewaretoken: token,
                    post_id: postPK,
					commented: commented
                },
                success: function (response) {
					console.log('Post like successfully');
                },
                error: function (xhr, status, error) {
					switch (xhr.status) {
						case 401:
							window.location.replace("signinURL");
						default:
							console.log('Error like post:', error)
					}

                    console.log('Error like post:', error)
                }
            });

			$(this).children('i').toggleClass("far fa");
			$(this).children('h3').text(function(_,cur) {
				if ($(this).next().hasClass('far')) {
					console.log("working")
					if (cur > 0) return Number(cur) - 1
				}
				return Number(cur) + 1
			})

	    })
	//comment on post
	$('.comment-btn').on('click', function(e) {
		e.preventDefault();
		var commentForm = $(this).prev('.commentForm');
		var commentInput = commentForm.find('input').val()
		var postElement = $(document).find('.work-item');
		console.log(postElement)
		var postPK = postElement.data('post-pk');
		var postID = postPK;
		var host = window.location.host;
		var url = '//' + host + `/blog/post/${postID}/comment/`;
		var token = $(this).parent().data('token');
		//find reply id
		commentToggle = $(this).closest('.comment-toggle')
		reply_id = commentToggle.data('post-pk')
	
		// Make the AJAX request
		$.ajax({
		  type: 'POST',
		  url: url, 
		  data: {
			csrfmiddlewaretoken: token,
			content: commentInput,
			reply_id: reply_id
		  },
		  success: function(response) {
			console.log('Comment added successfully');
			location.reload();
		  },
		  error: function(error) {
			console.log('Error:', error);
		  }
		});
	  });
	//comment on reply

	$('.reply-button').on('click', function() {
		var replySection = $(this).closest('.commented-section');
		var pkSection = $(this).closest('.reply-section');
		var postPK = pkSection.data('post-pk');
		var commentForm = replySection.nextAll('.comment-toggle').first();
		
		commentForm.attr('data-post-pk', postPK);
		commentForm.toggle();
	  });

})(jQuery);