# network
## Introduction
It's a Twitter-like social network website for making posts and following users.

![display](https://github.com/jim37500/network/blob/main/deplay/display.png)


## Getting Started
1. In your terminal, cd into the project4 directory.
2. Run python manage.py makemigrations network to make migrations for the network app.
3. Run python manage.py migrate to apply migrations to your database.

## Specification
- **New Post:** Users who are signed in should be able to write a new text-based post by filling in text into a text area and then clicking a button to submit the post.
  - The screenshot at the top of this specification shows the “New Post” box at the top of the “All Posts” page.

- **All Posts:** The “All Posts” link in the navigation bar should take the user to a page where they can see all posts from all users, with the most recent posts first.
  - Each post should include the username of the poster, the post content itself, the date and time at which the post was made, and the number of “likes” the post has.

- **Profile Page:** Clicking on a username will load that user’s profile page. This page will:
  - Display the number of followers the user has, as well as the number of people that the user follows.
  - Display all of the posts for that user, in reverse chronological order.
  - For any other user who is signed in, this page will also display a “Follow” or “Unfollow” button that will let the current user toggle whether or not they are following this user’s posts. Note that this only applies to any “other” user: a user should not be able to follow themselves.

- **Following:** The “Following” link in the navigation bar should take the user to a page where they see all posts made by users that the current user follows.

- **Pagination:** On any page that displays posts, posts should only be displayed 10 on a page. If there are more than ten posts, a “Next” button should appear to take the user to the next page of posts (which should be older than the current page of posts). If not on the first page, a “Previous” button should appear to take the user to the previous page of posts as well.

- **Edit Post:** Users will be able to click an “Edit” button or link on any of their own posts to edit that post.

- **“Like” and “Unlike”:** Users will be able to click a button or link on any post to toggle whether or not they “like” that post.

- **Comment:** Users will be able to click a button to comment on the post.





  


 
