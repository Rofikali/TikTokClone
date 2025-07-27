
// // Still not in User 

// // stores/loadMore.js
// import { defineStore } from 'pinia'
// import { useNuxtApp } from '#app'
// import { createCursorStore } from '~/stores/utils/cursorStoreFactory'
// // stores/utils/cursorStoreFactory.js
// // This store uses the cursorStoreFactory to create a feed store that handles pagination

// import { defineStore } from 'pinia'
// import { createCursorStore } from './utils/cursorStoreFactory'
// import { useNuxtApp } from '#app'

// export const useFollowersStore = defineStore('followers', () => {
//     const { $axios } = useNuxtApp()
//     return createCursorStore({
//         name: 'followers',
//         fetchFn: (cursor) => $axios.get('/api/followers/', {
//             params: { cursor, page_size: 10 }
//         })
//     })()
// })
