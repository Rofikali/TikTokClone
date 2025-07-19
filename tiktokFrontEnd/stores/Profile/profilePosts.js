

// // stores/Profile/profilePosts.js
// import { defineStore } from 'pinia'
// import { useNuxtApp } from '#app'
// import { createCursorStore } from '~/stores/utils/cursorStoreFactory'
// import { computed } from 'vue'

// export const useProfilePostsStore = defineStore('profilePosts', () => {
//     const { $axios } = useNuxtApp()
//     let userId = null

//     const store = createCursorStore({
//         name: 'profilePosts',
//         fetchFn: async (cursor) => {
//             try {
//                 const res = await $axios.get(`/api/profile/${userId}/posts/`, {
//                     params: { cursor, page_size: 10 }
//                 })

//                 console.log(`📦 Profile posts API response for user ${userId} with cursor ${cursor}:`, res.data)

//                 return res
//             } catch (err) {
//                 console.error('❌ Failed to fetch profile posts:', err)
//                 throw err
//             }
//         }
//     })()

//     const loadProfilePosts = async (newUserId) => {
//         userId = newUserId
//         console.log('🔄 Loading profile posts for user ID:', userId)
//         store.reset()
//         console.log('reseting store here', store.reset())
//         await store.fetchItems()
//         console.log('store.fetchItems() completed:', store.fetchItems())
//     }

//     const allLikes = computed(() =>
//         store.items.value.reduce((sum, post) =>
//             sum + (Array.isArray(post.likes) ? post.likes.length : 0), 0
//         )
//     )


//     return {
//         ...store,
//         loadProfilePosts,
//         allLikes
//     }
// })


import { defineStore } from 'pinia'
import { useNuxtApp } from '#app'
import { useRoute } from 'vue-router'
import { computed } from 'vue'
import { createCursorStore } from '~/stores/utils/cursorStoreFactory'

export const useProfilePostsStore = defineStore('profilePosts', () => {
    const { $axios, $userStore } = useNuxtApp()
    const route = useRoute()
    let userId = null

    const store = createCursorStore({
        name: 'profilePosts',
        fetchFn: async (cursor) => {
            if (!userId) {
                throw new Error('❌ userId is not set before fetching profile posts.')
            }

            const res = await $axios.get(`/api/profile/${userId}/posts/`, {
                params: { cursor, page_size: 10 }
            })

            console.log(`📦 Fetched profile posts for user ${userId}:`, res.data)
            return res
        }
    })()

    const loadProfilePosts = async (newUserId = null) => {
        if (!newUserId) {
            const user = await $userStore.getUser()
            newUserId = user?.id

            if (!newUserId) {
                console.warn('⚠️ User ID not found after login')
                return
            }
        }

        userId = newUserId
        console.log('🔄 Loading profile posts for user ID:', userId)

        store.reset()
        await store.fetchItems()
    }

    const allLikes = computed(() =>
        store.items.value.reduce(
            (sum, post) => sum + (Array.isArray(post.likes) ? post.likes.length : 0),
            0
        )
    )

    return {
        ...store,
        loadProfilePosts,
        allLikes
    }
})
