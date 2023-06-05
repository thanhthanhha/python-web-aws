
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

	$(document).ready(function() {
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
	});

})(jQuery);