$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", $('meta[name=csrf-token]').attr('content'));
        }
    }
});

$(document).ready(function () {
    $('.like-button').on('click', function () {
        const postId = $(this).data('post-id');

        $.post(`/like/${postId}`, function (data) {
            $(`#likes-btn-${postId}`).text(data.likes);
        });
    });
});

$(document).ready(function () {
    $(".post-comment").on("click", function () {
        const inputField = $(".comment-input");
        const comment = inputField.val().trim();
        const postId = inputField.data("post-id");

        if (!comment) return;

        $.ajax({
            url: "/comment",
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify({ comment: comment, post_id: postId }),
            success: function (response) {
                if (response.status === "success") {
                    const newCommentHtml = `
                        <div class="comment">
                            <h3>${response.comment.username}</h3>
                            <p>${response.comment.content}</p>
                        </div>
                    `;
                    $("#comments").append(newCommentHtml);
                    inputField.val(""); // clear input
                }
            },
            error: function (xhr) {
                alert("Failed to post comment.");
            }
        });
    });
});