<template>
    <MainLayout>
        <div v-if="$profileStore.name"
            class="pt-[90px] 2xl:pl-[185px] lg:pl-[160px] lg:pr-0 pr-2 w-[calc(100%-90px)] max-w-[1800px] 2xl:mx-auto">
            <!-- Profile Header -->
            <div class="flex w-[calc(100vw-230px)]">
                <NuxtImg class="max-w-[120px] rounded-full" :src="$profileStore.image" width="120" height="120"
                    alt="Profile Image" loading="lazy" />
                <div class="ml-5 w-full">
                    <div class="text-[30px] font-bold truncate">
                        {{ $generalStore.allLowerCaseNoCaps($profileStore.name) }}
                    </div>
                    <div class="text-[18px] truncate">
                        {{ $profileStore.username }}
                    </div>

                    <button v-if="$profileStore.id === $userStore.id" @click="$generalStore.isEditProfileOpen = true"
                        class="flex item-center rounded-md py-1.5 px-3.5 mt-3 text-[15px] font-semibold border hover:bg-gray-100">
                        <Icon class="mt-0.5 mr-1" name="mdi:pencil" size="18" />
                        <div>Edit profile</div>
                    </button>

                    <button v-else
                        class="flex item-center rounded-md py-1.5 px-8 mt-3 text-[15px] text-white font-semibold bg-[#F02C56]">
                        Follow
                    </button>
                </div>
            </div>

            <!-- Stats -->
            <div class="flex items-center pt-4">
                <div class="mr-4">
                    <span class="font-bold">10K</span>
                    <span class="text-gray-500 font-light text-[15px] pl-1.5">Following</span>
                </div>
                <div class="mr-4">
                    <span class="font-bold">44K</span>
                    <span class="text-gray-500 font-light text-[15px] pl-1.5">Followers</span>
                </div>
                <div class="mr-4">
                    <span class="font-bold">{{ allLikes }}</span>
                    <span class="text-gray-500 font-light text-[15px] pl-1.5">Likes</span>
                </div>
            </div>

            <!-- Bio -->
            <div class="pt-4 mr-4 text-gray-500 font-light text-[15px] pl-1.5 max-w-[500px]">
                {{ $profileStore.bio }}
            </div>

            <!-- Tabs -->
            <div class="w-full flex items-center pt-4 border-b">
                <div class="w-60 text-center py-2 text-[17px] font-semibold border-b-2 border-b-black">
                    Videos
                </div>
                <div class="w-60 text-gray-500 text-center py-2 text-[17px] font-semibold">
                    <Icon name="material-symbols:lock-open" class="mb-0.5" /> Liked
                </div>
            </div>

            <!-- Posts Grid -->
            <div v-if="posts.length > 0"
                class="mt-4 grid 2xl:grid-cols-6 xl:grid-cols-5 lg:grid-cols-4 md:grid-cols-3 grid-cols-2 gap-3">
                <PostUser v-for="post in posts" :key="post.id" :post="post" />
            </div>
            <div v-else class="text-gray-500 text-center mt-5 px-5">No posts found</div>

            <!-- 🔥 Add this to trigger IntersectionObserver -->
            <div ref="target" class="h-6 w-full"></div>

            <div v-if="loading" class="text-center text-sm text-gray-400 mt-4">
                Loading more posts...
            </div>



        </div>
    </MainLayout>
</template>

<script setup>
import MainLayout from '~/layouts/MainLayout.vue'
import { storeToRefs } from 'pinia'
import { useProfileStore } from '~/stores/Profile/profile'
import { useProfilePostsStore } from '~/stores/Profile/profilePosts'
import { useObserver } from '~/stores/utils/observer'

const { $userStore, $generalStore } = useNuxtApp()
const profileStore = useProfileStore()
const postStore = useProfilePostsStore()

const {
    items: posts,
    allLikes,
    // fetchItems,
    hasMore,
    loading,
} = storeToRefs(postStore)

const { fetchItems } = postStore

const route = useRoute()
definePageMeta({ middleware: 'auth' })

// Debug logs
console.log('📄 This is profile page')
console.log('🧾 Posts:', posts)
console.log('❤️ Likes:', allLikes)
console.log('🔁 hasMore:', hasMore)
console.log('⏳ loading:', loading)
// console.log('📥 fetchItems:', fetchItems)

onMounted(async () => {
    await profileStore.getProfile(route.params.id)
    await postStore.loadProfilePosts(route.params.id)
 
    console.log('✅ Finished onMounted. hasMore:', hasMore.value)
})

// Infinite scroll logic
const loadMore = () => {
    console.log('👀 Observer triggered')
    if (!loading.value && hasMore.value) {
        console.log('📥 Fetching more...')
        fetchItems() // <-- call directly, no `.value`
    } else {
        console.log('🚫 Not fetching (loading or no more)')
    }
}


const { target } = useObserver(loadMore, { threshold: 0.6 })
</script>
