## 1. uv venv
source .venv/Scripts/activate

## 2. install all requirements.txt data
uv pip install -r requirements.txt 

## To Install From an Existing pyproject.toml
uv pip install -r pyproject.toml

## all in one
python manage.py makemigrations accounts like comments postsapi core pagination search
python manage.py migrate
python manage.py createsuperuser

## generate fake posts with videos
python manage.py generate_posts

## generate fake user with videos
python manage.py generate_users

## generate fake user with videos
python manage.py generate_likes


## DB Issues
  ----> ble to open database file
            ls -la /workspaces/TikTokClone/tiktokApi/database
          mkdir -p database

## Delete pyc ( pycache )
  find . -name "*.pyc" -delete

## Run Commands Development
  python manage.py runserver

  Production
      export ENVIRONMENT=production
      python manage.py runserver

  GitHub Codespaces:
      ENVIRONMENT=production python manage.py runserver






# django rest apis
/backend/
├── apps/
│   ├── accounts/                # user registration, login, profiles, followers
│   │   ├── models/
│   │   ├── views/
│   │   ├── serializers/
│   │   ├── urls.py
│   │   └── tasks/               # Celery async tasks (e.g. follow notifications)
│
│   ├── posts/                   # video posts, likes, comments
│   │   ├── models/
│   │   ├── views/
│   │   ├── serializers/
│   │   ├── urls.py
│   │   └── signals/             # signal handlers (e.g. update like counts)
│
│   ├── notifications/               # reusable WebSocket logic
│   │   ├── consumers
          ├── consumers.py
        ├── routers
          ├── routing.py
│   │   ├── middlewares.py
│   │   └── utils.py
│
│   ├── common/                 # reusable components
│   │   ├── utils/
│   │   ├── mixins/
│   │   ├── pagination/
│   │   └── permissions/
│
├── backend/                     # Django settings split by env
│   ├── settings/
│   │   ├── base.py
│   │   ├── dev.py
│   │   ├── prod.py
│   ├── urls.py
│   ├── asgi.py                 # for Channels
│   └── wsgi.py
│
├── routing.py                  # WebSocket top-level routing
├── manage.py
├── requirements/
│   ├── base.txt
│   ├── dev.txt
│   ├── prod.txt
└── .env

# Nuxt3 frontend with Javascript
/frontend/
├── components/              
│   │   ├── register.vue
│   │   ├── login.vue
│   │   ├── sidebar.vue
│   │   ├── upload.vue
│   │   └── 
│
│   ├── layouts/       
│   │   ├── mainlayout.vue
│   │   ├── uploadlayout.vue
│
│   ├── middleware/      
│   │   ├── auth.js
│
│   ├── plugins/               
│   │   ├── axios.js
│   │   ├── stores.js
│
├── stores/                    
│   ├── profile/
│   │   ├── profile.js
│   │   ├── profilePosts.js
├   ├── utils/
│       ├── cursorstorefactory.js
│       ├── observer.js
        ├── debounce.js       # i will do use and work on it later.  WebSocket top-level routing
    ├── sockets/               #   WebSocket top-level routing
│       ├── likes.js
│       ├── followers.js
├── search.js                  
├── user.js

├── pages/
│   ├── post/
│   ├      /[id].vue
│   ├── profile/
            /[id].vue
    inde.vue

gonna host to railway 
hork home
going to modularize uis
going to start adding django channels
