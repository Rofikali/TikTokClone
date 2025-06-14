<script setup>
import { ref, watch, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { Cropper, CircleStencil } from 'vue-advanced-cropper'
import 'vue-advanced-cropper/dist/style.css'
import { storeToRefs } from 'pinia'

const { $userStore, $generalStore, $profileStore } = useNuxtApp()
const { name, bio, image } = storeToRefs($userStore)
const route = useRoute()

// Reactive state
const file = ref(null)
const cropper = ref(null)
const uploadedImage = ref(null)
const userImage = ref(null)
const Name = ref('')
const userName = ref('')
const userBio = ref('')
const isUpdated = ref(false)

// Initialize local state from store on mount
onMounted(() => {
    userName.value = name.value
    userBio.value = bio.value
    userImage.value = image.value
})

// Handle file input and create object URL for cropper
function getUploadedImage(event) {
    const selectedFile = event.target.files[0]
    if (!selectedFile) return
    file.value = selectedFile
    uploadedImage.value = URL.createObjectURL(selectedFile)
}

// Crop image and update user profile image
async function cropAndUpdateImage() {
    try {
        const { coordinates } = cropper.value.getResult()
        const data = new FormData()

        data.append('image', file.value)
        data.append('height', coordinates.height || '')
        data.append('width', coordinates.width || '')
        data.append('left', coordinates.left || '')
        data.append('top', coordinates.top || '')

        await $userStore.updateUserImage(data)
        await $userStore.getUser()
        await $profileStore.getProfile(route.params.id)

        // Update side menu images based on new user data
        $generalStore.updateSideMenuImage($generalStore.suggested, $userStore)
        $generalStore.updateSideMenuImage($generalStore.following, $userStore)

        // Update local image and clear upload state
        userImage.value = image.value
        uploadedImage.value = null
    } catch (error) {
        console.error(error)
    }
}

// Update user info (username and bio)
async function updateUserInfo() {
    try {
        await $userStore.updateUser(userName.value, userBio.value)
        await $userStore.getUser()
        await $profileStore.getProfile(route.params.id)

        userName.value = name.value
        userBio.value = bio.value

        setTimeout(() => {
            $generalStore.isEditProfileOpen = false
        }, 100)
    } catch (error) {
        console.error(error)
    }
}

// Watch for changes on username and bio to toggle "Save" button
watch([userName, userBio], ([newUserName, newUserBio]) => {
    const nameChanged = newUserName && newUserName !== name.value
    const bioValid = newUserBio && newUserBio.length > 0
    isUpdated.value = nameChanged || bioValid
})
</script>
