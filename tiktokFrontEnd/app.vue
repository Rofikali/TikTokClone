<template>
    <NuxtLayout>
        <NuxtPage />
    </NuxtLayout>

    <AuthOverlay v-if="isLoginOpen" />
    <EditProfileOverlay v-if="isEditProfileOpen" />
</template>

<script setup>
import { onMounted, watch } from 'vue'
import { storeToRefs } from 'pinia'
import { useUserStore } from '~/stores/user'
import { useGeneralStore } from '~/stores/general'

const $userStore = useUserStore()
const $generalStore = useGeneralStore()

const { isLoginOpen, isEditProfileOpen } = storeToRefs($generalStore)

onMounted(async () => {
    $generalStore.bodySwitch(false)
    isLoginOpen.value = false
    isEditProfileOpen.value = false

    try {
        await $generalStore.hasSessionExpired()
        await $generalStore.getRandomUsers('suggested')
        await $generalStore.getRandomUsers('following')

        if ($userStore.id) {
            await $userStore.getUser()
        }
    } catch (error) {
        console.error(error)
    }
})

watch(() => isLoginOpen.value, (val) => $generalStore.bodySwitch(val))
watch(() => isEditProfileOpen.value, (val) => $generalStore.bodySwitch(val))
</script>
<style scoped>
body {
    overflow: hidden;
    background-color: #353434;
    color: white;
}
</style>