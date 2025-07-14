// stores/profile.js
import { defineStore } from 'pinia'
import axios from '../plugins/axios'
import { ref, computed } from 'vue' // 👈 make sure computed is imported

const $axios = axios().provide.axios

export const useProfileStore = defineStore('profile', () => {
  const id = ref('')
  const name = ref('')
  const username = ref('')
  const bio = ref('')
  const image = ref('')
  const post = ref(null)
  const posts = ref([])

  // ✅ Automatically computed from posts
  const allLikes = computed(() => {
    return posts.value.reduce((total, post) => {
      return total + (Array.isArray(post.likes) ? post.likes.length : 0)
    }, 0)
  })

  async function getProfile(userId) {
    try {
      const res = await $axios.get(`/api/profile/${userId}/`)
      console.log('✅ Profile response:', res.data)

      const { user, posts: userPosts } = res.data

      if (!user) {
        console.warn('⚠️ No user object returned from profile API')
        return
      }

      id.value = user.id || ''
      name.value = user.name || user.username || ''
      username.value = user.username || ''
      bio.value = user.bio || ''
      image.value = user.image || ''
      posts.value = userPosts || []

      return { user, posts: userPosts }

    } catch (error) {
      console.error('❌ Failed to fetch profile:', error)
      return null
    }
  }

  function reset() {
    id.value = ''
    name.value = ''
    username.value = ''
    bio.value = ''
    image.value = ''
    post.value = null
    posts.value = []
    // ❌ you don't need to reset allLikes anymore — it's computed
  }

  return {
    id,
    name,
    username,
    bio,
    image,
    post,
    posts,
    allLikes, // ✅ include computed in the returned object
    getProfile,
    reset,
  }
}, {
  persist: true,
})
