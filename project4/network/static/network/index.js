document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".js-edit-btn").forEach((element, index) => {
    element.addEventListener('click', () => {
      element.classList.add('invisible');
      const { postId } = element.dataset;
      document.querySelector(`#post-id${postId}-content`).classList.add('invisible');
      getPost(postId, element);
    })
  });

  document.querySelectorAll(".js-like-btn").forEach(element => {
    const { postId } = element.dataset;
    getLikePostorNot(element, postId);
    element.addEventListener('click', () => { 
      fetch(`posts/${postId}/like/`, {
        method: 'POST'
      })
      .then(response => response.json())
      .then(data => {
        if (data.is_like) {
          element.textContent = 'Unlike';
          element.classList.remove('btn-outline-primary');
          element.classList.add('btn-primary');
        } else {
          element.textContent = 'Like';
          element.classList.add('btn-outline-primary');
          element.classList.remove('btn-primary');
        }
        document.querySelector(`#post-id${postId}-count-likes`).innerHTML = `${data.likes} Likes`;
      })
      .catch(error => {
        console.error('Error:', error)
      });
    });
  });

  document.querySelectorAll('.js-comment-btn').forEach(element => {
    element.addEventListener('click', () => {
      const { postId } = element.dataset;
      element.classList.remove('btn-outline-primary');
      element.classList.add('btn-outline-success');
      document.querySelector(`#post-id${postId}-comments`).classList.remove('invisible');
      document.querySelector(`#post-id${postId}-add-comment`).innerHTML = `
        <input class="form-control form-control-sm" id="post-id${postId}-comment-text" name="content" rows="1" placeholder="Comment"></input>
        <div class="btn-group btn-group-sm mt-2" role="group" aria-label="Small button group">
          <button type="button" class="btn btn-primary" id="comment-btn${postId}">Comment</button>
          <button type="button" class="btn btn-outline-danger" id="comment-cancel-btn${postId}">Cancel</button>
        </div>
      `

      document.querySelector(`#comment-btn${postId}`).addEventListener('click', () => {
        addComment(postId);
      });

      document.querySelector(`#comment-cancel-btn${postId}`).addEventListener('click', () => {
        document.querySelector(`#post-id${postId}-comment-text`).value = '';
        document.querySelector(`#post-id${postId}-comments`).classList.add('invisible');
        element.classList.add('btn-outline-primary');
        element.classList.remove('btn-outline-success');
        document.querySelector(`#post-id${postId}-add-comment`).innerHTML = '';
      })
    });
  });
});


function getPost(post_id, element) {
  fetch(`posts/${post_id}/edit/`)
  .then(response => response.json())
  .then(post => {
    document.querySelector(`#post-id${post_id}`).innerHTML = `
      <textarea class="form-control" id="post-content${post_id}" name="content" rows="3">${post.content}</textarea>
      <div class="btn-group btn-group-sm my-2" role="group" aria-label="Small button group">
        <button type="button" class="btn btn-secondary" id="save-btn${post_id}">Save</button>
        <button type="button" class="btn btn-outline-secondary" id="cancel-btn${post_id}">Cancel</button>
      </div>
    `

    document.querySelector(`#save-btn${post_id}`).onclick = () => {
      editPost(post_id);
      element.classList.remove('invisible');
      document.querySelector(`#post-id${post_id}`).innerHTML = '';
      document.querySelector(`#post-id${post_id}-content`).classList.remove('invisible');
    }

    document.querySelector(`#cancel-btn${post_id}`).onclick = () => {
      element.classList.remove('invisible');
      document.querySelector(`#post-id${post_id}`).innerHTML = '';
      document.querySelector(`#post-id${post_id}-content`).classList.remove('invisible');
    }
  })
  .catch(error => {
    console.log('Error:', error);
  })
}

function editPost(post_id) {
  fetch(`posts/${post_id}/edit/`, {
    method:'PUT',
    body: JSON.stringify({
      content: document.querySelector(`#post-content${post_id}`).value
    })
  })
  .then(response => response.json())
  .then(post => {
    document.querySelector(`#post-id${post_id}-content`).innerHTML = post.content;
  })
  .catch(error => {
    console.log('Error:', error);
  })
}


function getLikePostorNot(element, post_id) {
  fetch(`posts/${post_id}/like/`)
  .then(response => response.json())
  .then(data => {
    if (data.is_like) {
      element.classList.remove('btn-outline-primary');
      element.classList.add('btn-primary');
    }
  })
}


function addComment(postId) {
  const commentText = document.querySelector(`#post-id${postId}-comment-text`).value;

    fetch(`posts/${postId}/comment/`, {
    method: 'POST',
    body: JSON.stringify({
      content: commentText
    })
  })
  .then(response => response.json())
  .then(comment => {
    const commentDiv = document.createElement('div');
    commentDiv.classList.add('border', 'rounded', 'px-2', 'py-2', 'mt-2'); 
    const authorDiv = document.createElement('div');
    const authorA = document.createElement('a');
    authorA.href ='/profile/' + comment.user;
    authorA.classList.add('text-dark', 'comment-author');
    authorA.innerHTML = comment.user;
    authorDiv.appendChild(authorA);
    commentDiv.appendChild(authorDiv);

    const textDiv = document.createElement('div');
    textDiv.classList.add('comment-content');
    textDiv.innerHTML = comment.content;
    commentDiv.appendChild(textDiv);

    const timeDiv = document.createElement('div');
    timeDiv.classList.add('post-time', 'text-secondary');
    timeDiv.innerHTML = comment.create_time;
    commentDiv.appendChild(timeDiv);
    
    document.querySelector(`#post-id${postId}-comments`).appendChild(commentDiv);
    document.querySelector(`#post-id${postId}-comment-text`).value = '';

    const commentElement = document.querySelector(`#post-id${postId}-count-comments`)
    let count_comments = parseInt(commentElement.innerHTML);
    commentElement.innerHTML = `${count_comments + 1}`;

  })
  .catch(error => {
    console.error('Error adding comment:', error);
});

}