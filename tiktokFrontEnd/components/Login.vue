<template>
    <div class="text-center text-[28px] mb-4 font-bold">Log in</div>

    <form @submit.prevent="login">
        <!-- Email -->
        <div class="px-6 pb-1.5 text-[15px]">Email address</div>
        <div class="px-6 pb-2">
            <div class="relative">
                <input id="input-email" type="email" placeholder="Email address" :value="email" autocomplete="off"
                    autofocus @input="email = $event.target.value"
                    class="block w-full bg-[#F1F1F2] text-gray-800 border border-gray-300 rounded-md py-2.5 px-3 focus:outline-none" />
                <p v-if="errors?.email" class="text-red-500 text-sm mt-1">
                    {{ errors.email[0] }}
                </p>
            </div>
        </div>

        <!-- Password -->
        <div class="px-6 pb-2">
            <div class="relative">
                <input id="input-password" :type="isPasswordVisible ? 'text' : 'password'" placeholder="Password"
                    :value="password" autocomplete="off" @input="password = $event.target.value"
                    class="block w-full bg-[#F1F1F2] text-gray-800 border border-gray-300 rounded-md py-2.5 px-3 focus:outline-none pr-16" />
                <button type="button" @click="isPasswordVisible = !isPasswordVisible"
                    class="absolute inset-y-0 right-3 flex items-center text-sm text-gray-600 focus:outline-none">
                    {{ isPasswordVisible ? 'Hide' : 'Show' }}
                </button>
                <p v-if="errors?.password" class="text-red-500 text-sm mt-1">
                    {{ errors.password[0] }}
                </p>
            </div>
        </div>

        <!-- Forgot password -->
        <div class="px-6 text-[12px] text-gray-600">Forgot password?</div>

        <!-- Submit -->
        <div class="px-6 pb-2 mt-6">
            <button type="submit" :disabled="!email || !password"
                :class="(!email || !password) ? 'bg-gray-200' : 'bg-[#F02C56]'"
                class="w-full text-[17px] font-semibold text-white py-3 rounded-sm">
                Log in
            </button>
        </div>
    </form>
</template>


<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const { $userStore, $generalStore, $profileStore } = useNuxtApp()

const email = ref('')
const password = ref('')
const errors = ref(null)
const isPasswordVisible = ref(false)
const router = useRouter()

const login = async () => {
    errors.value = null
    try {
        console.log('💡 Starting login flow')

        await $userStore.getTokens()
        console.log('✅ CSRF token fetched')

        await $userStore.login(email.value, password.value)
        console.log('✅ User logged in')

        const user = await $userStore.getUser()
        const user_id = user?.id
        console.log(`🔍 User data fetched:`, user);
        console.log(`🔍 User ID: ${user_id}`);

        if (!user_id) {
            console.warn('⚠️ User ID not found after login')
            return
        }

        router.push({ name: 'profile-id', params: { id: user_id } })

        console.log('🔐 Login modal closed')
        $generalStore.isLoginOpen = false

    } catch (error) {
        console.error('❌ Error during login flow:', error)
        errors.value = error.response?.data?.errors || { general: ['Login failed'] }
    }
}

</script>
