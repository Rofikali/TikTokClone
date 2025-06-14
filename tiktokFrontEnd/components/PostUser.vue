

<template>
    <div @click="displayPost(post)" @mouseenter="isHover(true)" @mouseleave="isHover(false)"
        class="relative brightness-90 hover:brightness-[1.1] cursor-pointer">
        <div v-if="!isLoaded"
            class="absolute flex items-center justify-center top-0 left-0 aspect-[3/4] w-full object-cover rounded-md bg-black">
            <Icon class="animate-spin ml-1" name="mingcute:loading-line" size="100" color="#FFFFFF" />
        </div>
        <video ref="video" muted loop class="aspect-[3/4] object-cover rounded-md" :src="post.video" />
        <div class="px-1">
            <div class="text-gray-700 text-[15px] pt-1 break-words">
                {{ post.text }}
            </div>
            <div class="flex items-center -ml-1 text-gray-600 font-bold text-xs">
                <Icon name="gg:loadbar-sound" size="20" />
                3%
                <Icon class="ml-1" name="tabler:alert-circle" size="16" />
            </div>
        </div>
    </div>
</template>

<script setup>
const { $generalStore } = useNuxtApp()
const props = defineProps(['post'])
const { post } = toRefs(props)

const router = useRouter()
const route = useRoute()

const video = ref(null)
const isLoaded = ref(false)

onMounted(() => {
    if (video.value) {
        video.value.addEventListener('loadeddata', () => {
            setTimeout(() => {
                isLoaded.value = true
            }, 200)
        })
    }
})

onBeforeUnmount(() => {
    if (video.value) {
        video.value.pause()
        video.value.currentTime = 0
        video.value.src = ''
    }
})

const displayPost = (post) => {
    $generalStore.setBackUrl(`/profile/${route.params.id}`)
    $generalStore.selectedPost = null
    setTimeout(() => router.push(`/post/${post.id}`), 300)
}

const isHover = (bool) => {
    if (!video.value) return
    if (bool) {
        video.value.play()
    } else {
        video.value.pause()
    }
}
</script>
