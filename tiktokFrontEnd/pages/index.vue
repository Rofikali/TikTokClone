<!-- <template>
    <MainLayout>
        <div class="pt-[80px] w-[calc(100%-90px)] max-w-[690px]">
            <div v-for="post in $generalStore.posts" :key="post">
                <PostMain v-if="post" :post="post" />
            </div>
        </div>
    </MainLayout>
</template>

<script setup>
import MainLayout from '~/layouts/MainLayout.vue';
const { $generalStore } = useNuxtApp()
onMounted(async () => {
    try {
        $generalStore.getAllUsersAndPosts()
    } catch (error) {
        console.log(error)
    }
})
</script> -->

<!-- after pagination added to this page  -->

<!-- pages/index.vue -->
<template>
    <MainLayout>
        <!-- <div class="pt-[80px] w-[calc(100%-90px)] max-w-[690px] mx-auto"> -->
        <div class="pt-[80px] w-[calc(100%-90px)] max-w-[690px]">
            <PostMain v-for="(post, index) in feedStore.items" :key="post.id" :post="post"
                :isLastPost="index === feedStore.items.length - 1" />

            <div v-if="feedStore.loading" class="text-center text-gray-500 py-4">
                Loading more posts...
            </div>

            <div v-if="!feedStore.hasMore && feedStore.items.length" class="text-center text-gray-400 py-4">
                No more posts to load.
            </div>
        </div>
    </MainLayout>
</template>

<script setup>
import MainLayout from '~/layouts/MainLayout.vue'
import { useFeedStore } from '~/stores/loadMore'
import { onMounted } from 'vue'

const feedStore = useFeedStore()

onMounted(() => {
    if (feedStore.items.length === 0) {
        feedStore.fetchItems() // ✅ match actual method name
    }
})

</script>
