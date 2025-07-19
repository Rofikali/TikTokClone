
import { defineStore } from 'pinia'
import axios from '../plugins/axios'
import { useGeneralStore } from './general'

const $axios = axios().provide.axios

export const useUserStore = defineStore('user', () => {
  // State
  const id = ref('')
  const name = ref('')
  const username = ref('')
  const bio = ref('')
  const image = ref('')
  const email = ref('') // added because it’s used in `resetUser`

  // Actions

  async function getTokens() {
    await $axios.get('/api/csrftoken/')
  }

  async function login(userEmail, password) {
    console.log('🔐 login() called with:', { userEmail, password })

    try {
      const res = await $axios.post('/api/login/', {
        email: userEmail,
        password: password
      },
        { withCredentials: true }
      )



      console.log('✅ Login response received')
      console.log('📥 Response data:', res.data)
      console.log('📥 Response headers:', res.headers)

      // Log cookies available on client (for debugging)
      const sessionCookie = useCookie('sessionid').value
      const csrfCookie = useCookie('csrftoken').value

      console.log('🍪 Cookies after login:')
      console.log('   sessionid:', sessionCookie)
      console.log('   csrftoken:', csrfCookie)

      console.log('🧪 If sessionid is missing, session was not created on backend')

      return res.data
    } catch (err) {
      console.error('❌ Login failed')
      console.error('🛑 Error message:', err.message)
      console.error('📦 Error response:', err.response?.data)
      console.error('📥 Error headers:', err.response?.headers)
      return null
    }
  }

  async function register(name, userName, userEmail, password, confirmPassword) {
    await $axios.post('/api/registeruser/', {
      name: name,
      username: userName,
      email: userEmail,
      password: password,
      password_confirmation: confirmPassword,
    })
  }

  async function getUser() {
    console.log('🔍 Starting getUser() function')

    try {
      const res = await $axios.get('/api/loggedinuser/', {
        withCredentials: true,
      })

      const user = res.data.user_data

      if (!user || !user.id) {
        console.warn('⚠️ No user data found in response')
        return null
      }

      // Set store values
      id.value = user.id
      username.value = user.username
      bio.value = user.bio
      image.value = user.image
      email.value = user.email

      console.log('✅ User successfully set in store:', {
        id: id.value,
        username: username.value,
        bio: bio.value,
        image: image.value,
        email: email.value,
      })

      return user
    } catch (err) {
      console.error('❌ Error fetching user:', err.response?.data || err.message)
      return null
    }
  }


  async function updateUserImage(data) {
    return await $axios.post('/api/update/user_image/', data,
      {
        withCredentials: true,
        headers: {
          'Authorization': `Token ${useCookie('csrftoken').value}`,
          'X-CSRFToken': useCookie('csrftoken').value || ''
        }
      }
    )
  }

  async function updateUser(userName, userBio) {
    return await $axios.patch('/api/update/profile/', {
      username: userName,
      bio: userBio,
    },
      {
        withCredentials: true,
        headers: {
          'Authorization': `Token ${useCookie('csrftoken').value}`,
          'X-CSRFToken': useCookie('csrftoken').value || ''
        }
      }
    )
  }

  async function createPost(data) {
    return await $axios.post('/api/postcreate/',
      data,
      {
        withCredentials: true,
        headers: {
          'Authorization': `Token ${useCookie('csrftoken').value}`,
          'X-CSRFToken': useCookie('csrftoken').value || ''
        }
      },)
  }

  async function deletePost(post) {
    return await $axios.delete(`/api/postdelete/${post.id}/`, {
      withCredentials: true,
      headers: {
        'Authorization': `Token ${useCookie('csrftoken').value}`,
        'X-CSRFToken': useCookie('csrftoken').value || ''
      }
    })
  }

  async function addComment(post, comment) {
    const res = await $axios.post('/api/comments/post/',
      {
        post_id: post.id,
        comment,
      },
      {
        withCredentials: true,
        headers: {
          'Authorization': `Token ${useCookie('csrftoken').value}`,
          'X-CSRFToken': useCookie('csrftoken').value || ''
        }
      })
    if (res.status === 200) {
      await updateComments(post)
    }
  }


  async function deleteComment(post, commentId) {
    try {
      const res = await $axios.delete(
        `/api/commentdelete/${commentId}/`,
        {
          data: { post_id: post.id },            // ✅ Payload goes here
          withCredentials: true,
          headers: {
            'Authorization': `Token ${useCookie('csrftoken').value}`,
            'X-CSRFToken': useCookie('csrftoken').value || ''
          }
        }
      );

      if (res.status === 200) {
        await updateComments(post);
      } else {
        console.warn('Unexpected status:', res.status);
      }
    } catch (error) {
      console.error('Error deleting comment:', error);
    }
  }

  // async function updateComments(post) {
  //   const generalStore = useGeneralStore()
  //   const res = await $axios.get(`/api/profile/${post.user.id}/`)

  //   for (let updatedPost of res.data.posts) {
  //     if (post.id === updatedPost.id) {
  //       generalStore.selectedPost.comments = updatedPost.comments
  //     }
  //   }
  // }
  
  async function updateComments(post) {
    const generalStore = useGeneralStore()
    const res = await $axios.get(`/api/profile/${post.user.id}/`)

    const posts = res?.data?.posts

    if (Array.isArray(posts)) {
      for (let updatedPost of posts) {
        if (post.id === updatedPost.id) {
          generalStore.selectedPost.comments = updatedPost.comments
          break
        }
      }
    } else {
      console.warn('Expected an array for res.data.posts but got:', posts)
    }
  }



  async function likePost(post, isPostPage) {
    const generalStore = useGeneralStore()

    // const res = await $axios.post('/api/likes', {
    const res = await $axios.post('/api/like/post/', {
      post_id: post.id,
    }, {
      withCredentials: true,
      headers: {
        'Authorization': `Token ${useCookie('csrftoken').value}`,
        'X-CSRFToken': useCookie('csrftoken').value || ''
      }
    })

    const singlePost = isPostPage ? post : generalStore.posts.find(p => p.id === post.id)
    singlePost?.likes?.push(res.data.like)
  }

  async function unlikePost(post, isPostPage) {
    const generalStore = useGeneralStore()

    const singlePost = isPostPage ? post : generalStore.posts.find(p => p.id === post.id)

    const deleteLike = singlePost.likes.find(like => like.user_id === id.value)

    const res = await $axios.delete(`/api/likedelete/${deleteLike.id}/`,
      {
        withCredentials: true,
        headers: {
          'Authorization': `Token ${useCookie('csrftoken').value}`,
          'X-CSRFToken': useCookie('csrftoken').value || ''
        }
      })

    const index = singlePost.likes.findIndex(like => like.id === res.data.like.id)
    if (index !== -1) {
      singlePost.likes.splice(index, 1)
    }
  }


  async function logout() {

    try {
      const res = await $axios.post('/api/logout/', {
        withCredentials: true,
        headers: {
          'Authorization': `Token ${useCookie('csrftoken').value}`,
          'X-CSRFToken': useCookie('csrftoken').value || ''
        }
      }
      )
    } catch (error) {
      console.error('❌ Error during logout:', error.response?.data || error.message)
    }
  }

  function resetUser() {
    id.value = ''
    username.value = ''
    email.value = ''
    bio.value = ''
    image.value = ''
  }

  return {
    id,
    username,
    bio,
    image,
    email,
    // methods from here
    getTokens,
    login,
    register,
    getUser,
    updateUserImage,
    updateUser,
    createPost,
    deletePost,
    addComment,
    deleteComment,
    updateComments,
    likePost,
    unlikePost,
    logout,
    resetUser,
  }
}, {
  persist: true,
  // pinia persist for persist credentials
})
