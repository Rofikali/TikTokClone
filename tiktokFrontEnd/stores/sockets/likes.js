// // // stores/sockets/likes.js
// // import { defineStore } from 'pinia'

// // export const useLikesSocketStore = defineStore('likesSocket', () => {
// //     const ws = ref(null)
// //     const isConnected = ref(false)
// //     const likesUpdates = ref([])

// //     function connect(postId) {
// //         if (ws.value) {
// //             console.log(`[WebSocket] Already connected to /ws/posts/${postId}/likes/`)
// //             return
// //         }

// //         const url = `ws://localhost:8000/ws/posts/${postId}/likes/`
// //         console.log(`[WebSocket] Connecting to ${url}...`)

// //         ws.value = new WebSocket(url)

// //         ws.value.onopen = () => {
// //             console.log('[WebSocket] ✅ Connection established.')
// //             isConnected.value = true
// //         }

// //         ws.value.onmessage = (event) => {
// //             try {
// //                 const data = JSON.parse(event.data)
// //                 likesUpdates.value.push(data)
// //                 console.log('[WebSocket] 📩 Message received:', data)
// //             } catch (err) {
// //                 console.error('[WebSocket] ❌ Failed to parse message:', event.data)
// //             }
// //         }

// //         ws.value.onerror = (error) => {
// //             console.error('[WebSocket] 🚨 Connection error:', error)
// //         }

// //         ws.value.onclose = (event) => {
// //             console.warn('[WebSocket] 🔌 Disconnected.', {
// //                 code: event.code,
// //                 reason: event.reason,
// //                 wasClean: event.wasClean,
// //             })
// //             isConnected.value = false
// //             ws.value = null
// //         }
// //     }

// //     function disconnect() {
// //         if (ws.value) {
// //             console.log('[WebSocket] 🔒 Closing connection manually...')
// //             ws.value.close()
// //             ws.value = null
// //         } else {
// //             console.log('[WebSocket] 🚫 No active connection to close.')
// //         }
// //     }

// //     function sendLikeUpdate(payload) {
// //         if (ws.value && ws.value.readyState === WebSocket.OPEN) {
// //             console.log('[WebSocket] 📤 Sending like update:', payload)
// //             ws.value.send(JSON.stringify(payload))
// //         } else {
// //             console.warn('[WebSocket] ❗ Cannot send message. Connection is not open.')
// //         }
// //     }

// //     return {
// //         connect,
// //         disconnect,
// //         sendLikeUpdate,
// //         likesUpdates,
// //         isConnected
// //     }
// // })


// // stores/sockets/likes.js
// import { defineStore } from 'pinia'
// import { ref } from 'vue'

// export const useLikesSocketStore = defineStore('likesSocket', () => {
//     const ws = ref(null)
//     const isConnected = ref(false)
//     const messages = ref([])

//     function connect(postId) {
//         if (ws.value) return

//         const url = `ws://localhost:8000/ws/posts/${postId}/likes/`
//         console.log('[WS] Connecting to:', url)

//         ws.value = new WebSocket(url)

//         ws.value.onopen = () => {
//             console.log('[WS] Connected ✅')
//             isConnected.value = true
//         }

//         ws.value.onmessage = (event) => {
//             const data = JSON.parse(event.data)
//             console.log('[WS] Message from server:', data)
//             messages.value.push(data)
//         }

//         ws.value.onerror = (error) => {
//             console.error('[WS] Error:', error)
//         }

//         ws.value.onclose = () => {
//             console.warn('[WS] Disconnected ❌')
//             isConnected.value = false
//             ws.value = null
//         }
//     }

//     function disconnect() {
//         if (ws.value) {
//             ws.value.close()
//             ws.value = null
//         }
//     }

//     function sendMessage(message) {
//         if (ws.value && ws.value.readyState === WebSocket.OPEN) {
//             const payload = { message }
//             console.log('[WS] Sending:', payload)
//             ws.value.send(JSON.stringify(payload))
//         } else {
//             console.warn('[WS] Cannot send message, not connected')
//         }
//     }

//     return {
//         connect,
//         disconnect,
//         sendMessage,
//         messages,
//         isConnected
//     }
// })

// stores/sockets/likes.js
import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useLikesSocketStore = defineStore('likesSocket', () => {
    const ws = ref(null)
    const isConnected = ref(false)
    const likesUpdates = ref([])

    function connect(postId) {
        if (ws.value) {
            console.log('[WS] Already connected')
            return
        }

        const url = `ws://localhost:8000/ws/posts/${postId}/likes/`
        console.log('[WS] Connecting to:', url)
        ws.value = new WebSocket(url)

        ws.value.onopen = () => {
            console.log('[WS] ✅ Connected')
            isConnected.value = true
        }

        ws.value.onmessage = (event) => {
            console.log('[WS] 📩 Message received:', event.data)
            try {
                const data = JSON.parse(event.data)
                likesUpdates.value.push(data)
            } catch (e) {
                console.warn('[WS] JSON parse error:', e)
                likesUpdates.value.push({ message: event.data })
            }
        }

        ws.value.onerror = (error) => {
            console.error('[WS] ❌ Error:', error)
        }

        ws.value.onclose = () => {
            console.warn('[WS] 🔌 Disconnected')
            isConnected.value = false
            ws.value = null
        }
    }

    function disconnect() {
        if (ws.value) {
            console.log('[WS] Disconnecting...')
            ws.value.close()
            ws.value = null
        }
    }

    function sendLikeUpdate(payload) {
        if (ws.value && ws.value.readyState === WebSocket.OPEN) {
            console.log('[WS] 🚀 Sending:', payload)
            ws.value.send(JSON.stringify(payload))
        } else {
            console.warn('[WS] Cannot send message, not connected')
        }
    }

    return {
        connect,
        disconnect,
        // sendLikeUpdate,
        sendMessage: sendLikeUpdate, // 👈 alias
        likesUpdates,
        isConnected
    }
})
