// stores/useSearchStore.ts
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useNuxtApp } from '#app'
import debounce from 'lodash/debounce'
import { createCursorStore } from './utils/cursorStoreFactory'

export const useSearchStore = defineStore('search', () => {
    const query = ref('')
    const showDropdown = ref(false)
    const searched = ref(false)
    const highlightedIndex = ref(-1)

    const { $axios } = useNuxtApp()

    const fetchFn = async (cursor) => {
        const trimmed = query.value.trim()
        if (!trimmed) return { data: { results: [], next: null } }

        return await $axios.get('/api/usersearch/', {
            params: {
                q: trimmed,
                ...(cursor && { cursor }),
            },
        })
    }

    const baseStore = createCursorStore({ name: 'search', fetchFn })()
    const { items: results, loading, fetchItems, reset, hasMore } = baseStore

    const search = debounce(async () => {
        reset()
        showDropdown.value = true
        searched.value = true
        highlightedIndex.value = -1
        await fetchItems()
    }, 300)

    const clearSearch = () => {
        query.value = ''
        reset()
        showDropdown.value = false
        searched.value = false
        highlightedIndex.value = -1
    }

    const moveDown = () => {
        if (!showDropdown.value || results.value.length === 0) return
        highlightedIndex.value = (highlightedIndex.value + 1) % results.value.length
    }

    const moveUp = () => {
        if (!showDropdown.value || results.value.length === 0) return
        highlightedIndex.value =
            (highlightedIndex.value - 1 + results.value.length) % results.value.length
    }

    return {
        query,
        results,
        loading,
        showDropdown,
        searched,
        highlightedIndex,
        search,
        clearSearch,
        moveDown,
        moveUp,
        fetchItems,
        hasMore,
    }
})
