
import { defineStore } from 'pinia'
import { useUserStore } from './user'
import axios from '../plugins/axios'
import { ref } from 'vue'

const $axios = axios().provide.axios

export const useGeneralStore = defineStore('general', () => {
  const isLoginOpen = ref(false)
  const isEditProfileOpen = ref(false)
  const selectedPost = ref(null)
  const ids = ref(null)
  const isBackUrl = ref('/')
  const posts = ref(null)
  const suggested = ref(null)
  const following = ref(null)

  function bodySwitch(val) {
    document.body.style.overflow = val ? 'hidden' : 'visible'
  }

  function allLowerCaseNoCaps(str) {
    if (!str || typeof str !== 'string') return ''
    return str.split(' ').join('-').toLowerCase()
  }

  function setBackUrl(url) {
    isBackUrl.value = url
  }

  async function hasSessionExpired() {
    $axios.interceptors.response.use(
      (response) => response,
      (error) => {
        switch (error.response.status) {
          case 401:
          case 419:
          case 503:
            useUserStore().resetUser()
            window.location.href = '/'
            break
          case 500:
            alert('Oops, something went wrong! The team has been notified.')
            break
          default:
            return Promise.reject(error)
        }
      }
    )
  }

  async function getPostById(id) {
    const res = await $axios.get(`/api/posts/${id}/`)
    console.log('res.data: in getPostById', res.data);
    selectedPost.value = res.data.post[0]
    ids.value = res.data.ids
  }

  async function getRandomUsers(type) {
    const res = await $axios.get('/api/getrandomusers/')
    if (type === 'suggested') suggested.value = res.data.suggested
    if (type === 'following') following.value = res.data.following
    console.log('res.data: ', res.data);
    // console.log('sudgested users: ', suggested.value)
    // console.log('following users: ', following.value);
  }

  function updateSideMenuImage(array, user) {
    array.forEach((res) => {
      if (res.id === user.id) res.image = user.image
    })
  }

  async function getAllUsersAndPosts() {
    const res = await $axios.get('/api/home/')
    posts.value = res.data
  }

  return {
    isLoginOpen,
    isEditProfileOpen,
    selectedPost,
    ids,
    isBackUrl,
    posts,
    suggested,
    following,
    bodySwitch,
    allLowerCaseNoCaps,
    setBackUrl,
    hasSessionExpired,
    getPostById,
    getRandomUsers,
    updateSideMenuImage,
    getAllUsersAndPosts,
  }
}, {
  persist: true,
})


