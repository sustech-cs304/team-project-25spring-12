import { defineStore } from 'pinia'

interface UserState {
    accessToken: string
}

export const useUserStore = defineStore('user', {
    state: (): UserState => ({
        accessToken: '',
    }),

    actions: {
        setToken(token: string) {
            this.accessToken = token
            localStorage.setItem('access_token', token)
        },

        clearToken() {
            this.accessToken = ''
            localStorage.removeItem('access_token')
        },

        loadTokenFromStorage() {
            const token = localStorage.getItem('access_token')
            if (token) {
                this.accessToken = token
            }
        },
    },
})
