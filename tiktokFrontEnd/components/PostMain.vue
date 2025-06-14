
<template>
    <div :id="`PostMain-${post.id}`" class="flex border-b py-6">
        <div @click="isLoggedIn(post.user)" class="cursor-pointer">
            <img class="rounded-full max-h-[60px]" width="60" :src="post.user.image" alt="User Image" />
        </div>
        <div class="pl-3 w-full px-4">
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

            <div class="text-[15px] pb-0.5 break-words md:max-w-[400px] max-w-[300px]">
                {{ post.text }}
            </div>
            <div class="text-[14px] text-gray-500 pb-0.5">#fun #cool #SuperAwesome</div>

            <div class="text-[14px] pb-0.5 flex items-center font-semibold">
                <Icon name="mdi:music" size="17" />
                <div class="px-1">original sound - AWESOME</div>
                <Icon name="mdi:heart" size="20" />
            </div>

            <div class="mt-2.5 flex">
                <div @click="displayPost(post)"
                    class="relative min-h-[480px] max-h-[580px] max-w-[260px] flex items-center bg-black rounded-xl cursor-pointer">
                    <video v-if="post.video" ref="video" loop muted class="rounded-xl object-cover mx-auto h-full"
                        :src="post.video" />
                    <img class="absolute right-2 bottom-14" width="90" src="~/assets/images/tiktok-logo-white.png"
                        alt="TikTok Logo" />
                </div>

                <div class="relative mr-[75px]">
                    <div class="absolute bottom-0 pl-2">
                        <div class="pb-4 text-center">
                            <button @click="isLiked ? unlikePost(post) : likePost(post)"
                                class="rounded-full bg-gray-200 p-2 cursor-pointer" type="button"
                                :aria-pressed="isLiked" :aria-label="isLiked ? 'Unlike post' : 'Like post'">
                                <Icon name="mdi:heart" size="25" :color="isLiked ? '#F02C56' : ''" />
                            </button>
                            <span class="text-xs text-gray-800 font-semibold">{{ post.likes.length }}</span>
                        </div>

                        <div class="pb-4 text-center">
                            <div class="rounded-full bg-gray-200 p-2 cursor-pointer" role="button" tabindex="0">
                                <Icon name="bx:bxs-message-rounded-dots" size="25" />
                            </div>
                            <span class="text-xs text-gray-800 font-semibold">
                                {{ post.comments?.length || post.comment || 0 }}
                            </span>
                        </div>

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
import { ref, onMounted, onBeforeUnmount, computed } from 'vue'
import { useRouter, useNuxtApp } from '#imports'

const { $generalStore, $userStore } = useNuxtApp()
const props = defineProps({
    post: Object
})
console.log('props: post Object ', props.post);


const post = ref(props.post)

const router = useRouter()
const video = ref(null)

onMounted(() => {
    const observer = new IntersectionObserver(
        (entries) => {
            if (!video.value) return

            if (entries[0].isIntersecting) {
                console.log('Element is playing ' + post.value.id)
                video.value.play()
            } else {
                console.log('Element is paused ' + post.value.id)
                video.value.pause()
            }
        },
        { threshold: [0.6] }
    )

    const element = document.getElementById(`PostMain-${post.value.id}`)
    if (element) {
        observer.observe(element)
    } else {
        console.warn(`Element PostMain-${post.value.id} not found`)
    }
})

onBeforeUnmount(() => {
    if (video.value) {
        video.value.pause()
        video.value.currentTime = 0
        video.value.src = ''
    }
})

const isLiked = computed(() => {
    return post.value.likes.some(like => like.user_id === $userStore.id)
})

const likePost = async (post) => {
    if (!$userStore.id) {
        $generalStore.isLoginOpen = true
        return
    }
    try {
        await $userStore.likePost(post)
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
        await $userStore.unlikePost(post, false)
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
    // setTimeout(() => router.push(`/post/${post.id}`), 200)
    setTimeout(() => {
        router.push({ name: 'post-id', params: { id: post.id } })
        // $generalStore.selectedPost = post
    }, 200)
}
</script>
