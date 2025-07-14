

// stores/loadMore.js
import { defineStore } from 'pinia'
import { useNuxtApp } from '#app'
import { createCursorStore } from '~/stores/utils/cursorStoreFactory'
// stores/utils/cursorStoreFactory.js
// This store uses the cursorStoreFactory to create a feed store that handles pagination
export const useFeedStore = defineStore('feed', () => {
  const { $axios } = useNuxtApp()
  console.log('Feed store initialized:', useFeedStore())
  const store = createCursorStore({
    name: 'feed',
    fetchFn: (cursor) =>
      $axios.get('/api/home/', {
        params: { cursor, page_size: 10 },
      }),
  })() // <-- Don't forget to call it

  return store
})