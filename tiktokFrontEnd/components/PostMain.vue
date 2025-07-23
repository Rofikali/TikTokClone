<template>
    <div :id="`PostMain-${post.id}`" ref="observerTarget" class="flex border-b py-6">
        <!-- User Avatar -->
        <div @click="isLoggedIn(post.user)" class="cursor-pointer">
            <NuxtImg class="rounded-full max-h-[60px]" width="60" :src="post.user.image" alt="User Image"
                loading="lazy" />
        </div>

        <div class="pl-3 w-full px-4">
            <!-- Header: Name + Follow -->
            <div class="flex items-center justify-between pb-0.5">
                <button @click="isLoggedIn(post.user)" type="button" class="text-left">
                    <span class="font-bold hover:underline cursor-pointer">
                        {{ $generalStore.allLowerCaseNoCaps(post.user?.name) }}
                    </span>
                    <span class="text-[13px] text-light text-gray-500 pl-1 cursor-pointer">
                        {{ post.user.name }}
                    </span>
                </button>

                <button
                    class="border text-[15px] px-[21px] py-0.5 border-[#F02C56] text-[#F02C56] hover:bg-[#ffeef2] font-semibold rounded-md"
                    type="button">
                    Follow
                </button>
            </div>

            <!-- Post Text -->
            <div class="text-[15px] pb-0.5 break-words md:max-w-[400px] max-w-[300px]">
                {{ post.text }}
            </div>

            <!-- Tags -->
            <div class="text-[14px] text-gray-500 pb-0.5">#fun #cool #SuperAwesome</div>

            <!-- Music Info -->
            <div class="text-[14px] pb-0.5 flex items-center font-semibold">
                <Icon name="mdi:music" size="17" />
                <div class="px-1">original sound - AWESOME</div>
                <Icon name="mdi:heart" size="20" />
            </div>

            <!-- Video + Actions -->
            <div class="mt-2.5 flex">
                <!-- Video Box -->
                <div @click="displayPost(post)"
                    class="relative min-h-[480px] max-h-[580px] max-w-[260px] flex items-center bg-black rounded-xl cursor-pointer">
                    <video v-if="post.video" ref="video" loop muted class="rounded-xl object-cover mx-auto h-full"
                        :src="post.video" />
                    <img class="absolute right-2 bottom-14" width="90" src="~/assets/images/tiktok-logo-white.png"
                        alt="TikTok Logo" />
                </div>

                <!-- Actions -->
                <div class="relative mr-[75px]">
                    <div class="absolute bottom-0 pl-2">
                        <!-- Like -->
                        <div class="pb-4 text-center">
                            <button @click="isLiked ? unlikePost(post) : likePost(post)"
                                class="rounded-full bg-gray-200 p-2 cursor-pointer" type="button"
                                :aria-pressed="isLiked" :aria-label="isLiked ? 'Unlike post' : 'Like post'">
                                <Icon name="mdi:heart" size="25" :color="isLiked ? '#F02C56' : ''" />
                            </button>
                            <span class="text-xs text-gray-800 font-semibold">{{ post.likes.length }}</span>
                        </div>

                        <!-- Comment -->
                        <div class="pb-4 text-center">
                            <NuxtLink :to="{ name: 'post-id', params: { id: post.id } }"
                                class="inline-flex flex-col items-center cursor-pointer" role="button" tabindex="0"
                                @click.prevent="!$userStore.id">
                                <div class="rounded-full bg-gray-200 p-2">
                                    <Icon name="bx:bxs-message-rounded-dots" size="25" />
                                </div>
                                <span class="text-xs text-gray-800 font-semibold mt-1">
                                    {{ post.comments?.length || 0 }}
                                </span>
                            </NuxtLink>
                        </div>

                        <!-- Share -->
                        <div class="text-center">
                            <div class="rounded-full bg-gray-200 p-2 cursor-pointer" role="button" tabindex="0">
                                <Icon name="ri:share-forward-fill" size="25" />
                            </div>
                            <span class="text-xs text-gray-800 font-semibold">55</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, onUnmounted } from 'vue'
// import { useRouter, useNuxtApp } from '#imports'
import { useFeedStore } from '~/stores/loadMore'
import { useObserver } from '~/stores/utils/observer'


const { $generalStore, $userStore } = useNuxtApp()
const feedStore = useFeedStore()
const router = useRouter()

const props = defineProps({
    post: Object,
    isLastPost: Boolean,
})


// console.log('post.id ', props.post.id)
// console.log('post id ', props.post.id[0])

const video = ref(null)
const playing = ref(false)

const post = ref({
    ...props.post,
    comments: props.post?.comments || [],
    likes: props.post?.likes || [],
    user: props.post?.user || {},
})

// const pauseAllOtherVideos = () => {
//     const allVideos = document.querySelectorAll('video')
//     allVideos.forEach((v) => {
//         if (v !== video.value) v.pause()
//     })
// }

const handleIntersection = (entry) => {
    if (!video.value) return

    if (entry.isIntersecting && !playing.value) {
        playing.value = true
        console.log('▶️ Playing post', post.value.id)
        // pauseAllOtherVideos()
        video.value.play()

        if (props.isLastPost && feedStore.hasMore && !feedStore.loading) {
            console.log('📥 Loading next feed page...')
            feedStore.fetchItems()
        }
    } else if (!entry.isIntersecting && playing.value) {
        playing.value = false
        console.log('⏸️ Pausing post', post.value.id)
        video.value.pause()
    }
}

const { target: observerTarget } = useObserver(handleIntersection, { threshold: 0.6 })

const isLiked = computed(() => {
    return post.value?.likes?.some((like) => like.user_id === $userStore.id) || false
})

const likePost = async (post) => {
    if (!$userStore.id) {
        $generalStore.isLoginOpen = true
        return
    }
    try {
        await $userStore.likePost(post, true)
    } catch (error) {
        console.error(error)
    }
}

const unlikePost = async (post) => {
    if (!$userStore.id) {
        $generalStore.isLoginOpen = true
        return
    }
    try {
        await $userStore.unlikePost(post, true)
    } catch (error) {
        console.error(error)
    }
}

const isLoggedIn = (user) => {
    if (!$userStore.id) {
        $generalStore.isLoginOpen = true
        return
    }
    setTimeout(() => router.push(`/profile/${user.id}`), 200)
}

const displayPost = (post) => {
    if (!$userStore.id) {
        $generalStore.isLoginOpen = true
        return
    }
    $generalStore.setBackUrl('/')
    $generalStore.selectedPost = null
    setTimeout(() => {
        router.push({ name: 'post-id', params: { id: post?.id } })
    }, 200)
}



onUnmounted(() => {
    if (video.value) video.value.pause()
    playing.value = false
})

document.addEventListener('visibilitychange', () => {
    if (document.hidden && video.value) {
        video.value.pause()
        playing.value = false
    }
})
</script>
