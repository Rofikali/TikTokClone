<template>
    <div ref="searchBoxRef" class="relative hidden md:flex flex-col max-w-[380px] w-full">
        <div class="flex items-center bg-[#F1F1F2] p-1 rounded-full w-full">
            <input v-model="searchStore.query" @input="handleInput" @keydown.enter.prevent="handleEnter"
                @keydown.down.prevent="searchStore.moveDown" @keydown.up.prevent="searchStore.moveUp"
                :placeholder="placeholder"
                class="w-full pl-3 my-2 bg-transparent placeholder-[#838383] text-[15px] focus:outline-none" />

            <button v-if="searchStore.query && !searchStore.loading" @click="searchStore.clearSearch"
                class="text-gray-400 hover:text-gray-600 pr-2">
                <Icon name="ic:round-close" size="20" />
            </button>

            <div class="px-3 py-1 flex items-center border-l border-l-gray-300 cursor-pointer"
                :class="searchStore.query.trim() ? 'text-[#F02C56]' : 'text-[#A1A2A7]'" @click="handleInput">
                <Icon v-if="!searchStore.loading" name="ri:search-line" size="22" />
                <Icon v-else name="eos-icons:loading" size="22" class="animate-spin" />
            </div>
        </div>

        <ul v-if="searchStore.showDropdown"
            class="absolute top-full mt-1 w-full bg-white rounded-md shadow z-50 max-h-[250px] overflow-auto">
            <li v-if="!searchStore.loading && searchStore.results.length === 0 && searchStore.searched"
                class="px-4 py-2 text-gray-500 text-sm">
                No users found.
            </li>

            <li v-for="(user, index) in searchStore.results" :key="user.id" @click="goToProfile(user)" :class="[
                'flex items-center px-4 py-2 cursor-pointer hover:bg-gray-100 text-sm',
                index === searchStore.highlightedIndex ? 'bg-gray-100' : ''
            ]">
                <img :src="user.image || '/default-avatar.png'" alt="avatar"
                    class="w-8 h-8 rounded-full mr-3 object-cover" />
                <div>
                    <div class="font-medium">{{ user.username }}</div>
                    <div class="text-xs text-gray-500">{{ user.name }}</div>
                </div>
            </li>

            <!-- Infinite scroll sentinel -->
            <li ref="observerElement" class="h-1"></li>
        </ul>
    </div>
</template>


<script setup>
import { ref, onMounted, onBeforeUnmount, watch, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { debounce } from 'lodash-es'
import { useSearchStore } from '~/stores/search'

const props = defineProps({
    endpoint: String,
    placeholder: { type: String, default: 'Search accounts' },
})

const searchBoxRef = ref(null)
const observerElement = ref(null)
const router = useRouter()
const searchStore = useSearchStore()
let observer = null

// Debounced input search
const handleInput = debounce(() => {
    searchStore.search(props.endpoint)
}, 300)

const handleEnter = () => {
    if (searchStore.highlightedIndex >= 0) {
        goToProfile(searchStore.results[searchStore.highlightedIndex])
    } else if (searchStore.results.length === 1) {
        goToProfile(searchStore.results[0])
    }
}

const goToProfile = (user) => {
    searchStore.clearSearch()
    router.push(`/profile/${user.id}`)
}

const handleClickOutside = (event) => {
    if (!searchBoxRef.value?.contains(event.target)) {
        searchStore.showDropdown = false
    }
}

onMounted(() => {
    document.addEventListener('click', handleClickOutside)

    observer = new IntersectionObserver(
        (entries) => {
            const entry = entries[0]
            if (entry.isIntersecting && searchStore.hasMore && !searchStore.loading) {
                searchStore.fetchItems()
            }
        },
        { threshold: 0.5 }
    )

    if (observerElement.value) {
        observer.observe(observerElement.value)
    }
})

// ✅ Reobserve new element when results change
watch(() => searchStore.results.length, async () => {
    await nextTick()
    if (observer && observerElement.value) {
        observer.disconnect()
        observer.observe(observerElement.value)
    }
})

onBeforeUnmount(() => {
    document.removeEventListener('click', handleClickOutside)
    if (observer) {
        observer.disconnect()
    }
})
</script>
