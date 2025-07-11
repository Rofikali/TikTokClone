// stores/utils/observer.js
import { ref, onMounted, onUnmounted, watch } from 'vue'

export function useObserver(callback, options = {}) {
    const target = ref(null)
    let observer = null

    const defaultOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.6,
        ...options,
    }

    const start = () => {
        if (!target.value || typeof IntersectionObserver === 'undefined') return

        observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) callback(entry)
            })
        }, defaultOptions)

        observer.observe(target.value)
    }

    const stop = () => {
        if (observer && target.value) observer.unobserve(target.value)
        observer = null
    }

    onMounted(() => {
        if (target.value) start()
    })

    // ✅ React to late-binding `ref`
    watch(target, (el) => {
        if (el) start()
    })

    onUnmounted(stop)

    return {
        target,
        start,
        stop,
    }
}
