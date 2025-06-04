import {defineStore} from 'pinia'
import type {User} from '../types/user'
import type {Course} from '../types/course'
import type {Deadline} from "../types/deadline";

interface UserState extends User {
    courses: Course[] | null
    deadlines: Deadline[] | null
}

export const useUserStore = defineStore('user', {
    state: (): UserState => ({
        accessToken: '',
        username: '',
        is_admin: false,
        courses: null,
        deadlines: null,
    }),

    actions: {
        setToken(token: string) {
            this.accessToken = token
            localStorage.setItem('access_token', token)
        },

        setUsername(name: string) {
            this.username = name
            localStorage.setItem('username', name)
        },

        setAdmin(is_admin: boolean) {
            this.is_admin = is_admin
            localStorage.setItem('is_admin', is_admin.toString())
        },

        clearToken() {
            this.accessToken = ''
            this.username = ''
            this.courses = null
            this.deadlines = null
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

        setCourses(courseList: Course[]) {
            this.courses = courseList
        },

        setDeadlines(deadlineList: Deadline[]) {
            this.deadlines = deadlineList
        },
    },
})
