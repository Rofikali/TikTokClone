<template>
    <div id="SideNavMain" :class="route.fullPath === '/' ? 'lg:w-[310px]' : 'lg:w-[220px]'"
        class="fixed z-20 bg-white pt-[70px] h-full lg:border-r-0 border-r w-[75px] overflow-auto"
        @scroll.passive="handleScroll">
        <div class="lg:w-full w-[55px] mx-auto">
            <NuxtLink to="/">
                <MenuItem iconString="For You" colorString="#F02C56" sizeString="30" />
            </NuxtLink>
            <MenuItem iconString="Following" colorString="#000000" sizeString="27" />
            <MenuItem iconString="LIVE" colorString="#000000" sizeString="27" />

            <div class="border-b lg:ml-2 mt-2" />

            <div class="lg:block hidden text-xs text-gray-600 font-semibold pt-4 pb-2 px-2">
                Suggested accounts
            </div>

            <div class="lg:hidden block pt-3" />

            <template v-if="$generalStore.suggested && $generalStore.suggested.length">
                <div v-for="sug in $generalStore.suggested.slice(0, suggestedLimit)" :key="sug.id">
                    <div @click="isLoggedIn(sug)" class="cursor-pointer">
                        <MenuItemFollow :user="sug" />
                    </div>
                </div>
            </template>

            <button class="lg:block hidden text-[#F02C56] pt-1.5 pl-2 text-[13px]">
                See all
            </button>

            <div v-if="$userStore.id">
                <div class="border-b lg:ml-2 mt-2" />

                <div class="lg:block hidden text-xs text-gray-600 font-semibold pt-4 pb-2 px-2">
                    Following accounts
                </div>

                <div class="lg:hidden block pt-3" />

                <template v-if="$generalStore.following && $generalStore.following.length">
                    <div v-for="fol in $generalStore.following.slice(0, followingLimit)" :key="fol.id">
                        <div @click="isLoggedIn(fol)" class="cursor-pointer">
                            <MenuItemFollow :user="fol" />
                        </div>
                    </div>
                </template>

                <button class="lg:block hidden text-[#F02C56] pt-1.5 pl-2 text-[13px]">
                    See more
                </button>
            </div>

            <div class="lg:block hidden border-b lg:ml-2 mt-2" />

            <div class="lg:block hidden text-[11px] text-gray-500">
                <div class="pt-4 px-2">About Newsroom TikTok Shop Contact Careers ByteDance</div>
                <div class="pt-4 px-2">TikTok for Good Advertise Developers Transparency TikTok Rewards TikTok Browse
                    TikTok Embeds</div>
                <div class="pt-4 px-2">Help Safety Terms Privacy Creator Portal Community Guidelines</div>
                <div class="pt-4 px-2">© 2023 TikTok</div>
            </div>

            <div class="pb-14"></div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue'

const { $generalStore, $userStore } = useNuxtApp()
const route = useRoute()
const router = useRouter()

// Limits for lazy loading
const suggestedLimit = ref(10)
const followingLimit = ref(10)

const handleScroll = (e) => {
    const el = e.target
    if (el.scrollTop + el.clientHeight >= el.scrollHeight - 20) {
        // Lazy load more
        if ($generalStore.suggested && suggestedLimit.value < $generalStore.suggested.length) {
            suggestedLimit.value += 5
        }
        if ($generalStore.following && followingLimit.value < $generalStore.following.length) {
            followingLimit.value += 5
        }
    }
}

const isLoggedIn = (user) => {
    if (!$userStore.id) {
        $generalStore.isLoginOpen = true
        console.log('inside sideNav id ---->', $generalStore.id);
        return
    }
    setTimeout(() => router.push(`/profile/${user.id}`), 200)
}
</script>
<style scoped>
body {
    background-color: #a6f5f5;
    /* dark grey */
    color: rgb(44, 40, 40);
}
</style>