import { defineStore } from 'pinia'

interface UserState {
    accessToken: string
    username: string
}

export const useUserStore = defineStore('user', {
    state: (): UserState => ({
        accessToken: '',
        username: '',
    }),

    actions: {
        setToken(token: string) {
            this.accessToken = token
            localStorage.setItem('access_token', token)
        },

        clearToken() {
            this.accessToken = ''
            this.username = ''
            localStorage.removeItem('access_token')
            localStorage.removeItem('username')
        },

        loadTokenFromStorage() {
            const token = localStorage.getItem('access_token')
            const name = localStorage.getItem('username')
            if (token) {
                this.accessToken = token
            }
            if (name) {
                this.username = name
            }
        },

        setUsername(name: string) {
            this.username = name
            localStorage.setItem('username', name)
        },
    },
})
