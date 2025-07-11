// // stores/Profile/profile.js
// import { defineStore } from 'pinia'
// import axios from '~/plugins/axios'
// import { ref } from 'vue'

// const $axios = axios().provide.axios

// export const useProfileStore = defineStore('profile', () => {
//     const id = ref('')
//     const name = ref('')
//     const username = ref('')
//     const bio = ref('')
//     const image = ref('')

//     async function getProfile(userId) {
//         try {
//             const res = await $axios.get(`/api/profile/${userId}/`)
//             const user = res.data.user

//             if (!user) return

//             id.value = user.id || ''
//             name.value = user.name || user.username || ''
//             username.value = user.username || ''
//             bio.value = user.bio || ''
//             image.value = user.image || ''
//         } catch (error) {
//             console.error('❌ Failed to fetch profile:', error)
//         }
//     }

//     function reset() {
//         id.value = ''
//         name.value = ''
//         username.value = ''
//         bio.value = ''
//         image.value = ''
//     }

//     return {
//         id, name, username, bio, image,
//         getProfile,
//         reset
//     }
// })

// stores/Profile/profile.js
import { defineStore } from 'pinia'
import axios from '~/plugins/axios'
import { ref, computed } from 'vue'

const $axios = axios().provide.axios

export const useProfileStore = defineStore('profile', () => {
  const id = ref('')
  const name = ref('')
  const username = ref('')
  const bio = ref('')
  const image = ref('')
  const posts = ref([]) // hold initial batch of profile posts

  async function getProfile(userId) {
    try {
      const res = await $axios.get(`/api/profile/${userId}/`)
      const { user, posts: userPosts } = res.data

      if (!user) return

      id.value = user.id || ''
      name.value = user.name || user.username || ''
      username.value = user.username || ''
      bio.value = user.bio || ''
      image.value = user.image || ''
      // posts.value = userPosts || [] // load initial posts for display or like count

    } catch (error) {
      console.error('❌ Failed to fetch profile:', error)
    }
  }

  function reset() {
    id.value = ''
    name.value = ''
    username.value = ''
    bio.value = ''
    image.value = ''
    posts.value = []
  }

  return {
    id,
    name,
    username,
    bio,
    image,
    posts,
    // allLikes, // 👈 included here
    getProfile,
    reset,
  }
}, {
  persist: true,
})
