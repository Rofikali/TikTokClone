crete new route for 
    --> getting likes 
            --> nuxt3
            --> drf
            
----> Done ( Frontend - Backend )
    ---> Likes
    ---> Dislike
    --->    Not Done
        ---> Like Count with Username

Profile Problem Solved
    ---> 


Delete Comment --->


Error ---> 
        Edit Profile 
            ( Check )
                Learn from GS 
                    Make it working

Start Adding ---->
	ViewSets not ( ApiView )


**** All Posts Related Work Would in PostsApi Module  ****

*** suggested user / Following user ***

<!-- basdir/
    components
    plugins
    pages
    store
    middleware
    layouts
    components -->


/stores/
  /sockets/
    likes.js         ← Handles WebSocket for likes

  /profile/
    profile.js       ← User info (bio, etc.)
    posts.js         ← Cursor-based paginated posts
    likes.js         ← Paginated liked posts
    followers.js     ← Paginated followers
    following.js     ← Paginated followings

  /feed/
    main.js          ← Feed with cursor pagination
    trending.js      ← Trending posts (optional)

  /search/
    index.js         ← Debounced user search w/ filters

  /auth/
    session.js       ← Auth state (login/logout)

  /user/
    preferences.js   ← Settings, themes, etc.

/composables/
  useObserver.js     ← Infinite scroll IntersectionObserver
  useThrottle.js     ← Utility
  useDebounce.js     ← Utility

/pages/
  /profile/[id]/
    index.vue        ← Profile main view
    posts.vue        ← Profile’s posts
    likes.vue        ← Liked posts
    followers.vue    ← Followers
    following.vue    ← Followings

/components/
  PostCard.vue       ← Reusable video/post card
  LikeButton.vue     ← Emits like to socket & updates UI
  UserAvatar.vue     ← Reusable user profile image



templates/
    admin/
      includes/
        objects_tools.html
        submit_line.html
      base.html
      login.html
      logout.html
    registration
      login.html
      passowrd_change_done.html
      password_change_form.html
    static
      /admin/
        css/
          custom.css
        js/
          custom.js

setting.py
STATIC_ROOT = BASE_DIR / "static/"

tiktopApi/
  tiktopApi/
    settings/
      base.py
      ded.py

how use use dir /basedir/templates

