

// stores/utils/cursorStoreFactory.js
import { ref } from 'vue'

export function createCursorStore({ name, fetchFn }) {
    return () => {
        const items = ref([])
        const loading = ref(false)
        const nextCursor = ref(null)
        const hasMore = ref(true)

        const fetchItems = async () => {
            if (loading.value || !hasMore.value) return
            loading.value = true
            try {
                console.log(`[${name}] 🔄 Fetching items with cursor:`, nextCursor.value)
                const response = await fetchFn(nextCursor.value)
                const data = response.data

                if (Array.isArray(data.results)) {
                    items.value.push(...data.results)
                    console.log(`[${name}] ✅ Items after fetch:`, items.value)
                } else {
                    console.warn(`[${name}] ⚠️ Unexpected results structure:`, data)
                }

                if (data.next) {
                    const nextUrl = new URL(data.next, window.location.origin)
                    nextCursor.value = nextUrl.searchParams.get('cursor')
                    console.log(`[${name}] ➡️ Next cursor:`, nextCursor.value)
                } else {
                    nextCursor.value = null
                    console.log(`[${name}] 🛑 No more pages.`)
                }

                hasMore.value = !!data.next
            } catch (err) {
                console.error(`[${name}] ❌ Fetch failed:`, err)
            } finally {
                loading.value = false
            }
        }

        const reset = () => {
            items.value = []
            nextCursor.value = null
            hasMore.value = true
            console.log(`[${name}] ♻️ Store reset.`)
        }

        return {
            items,
            loading,
            nextCursor,
            hasMore,
            fetchItems,
            reset,
        }
    }
}
