import { defineStore } from 'pinia'
import type {User} from '../types/user'
import type {Course} from '../types/course'
import type {Deadline} from "../types/deadline";

interface UserState extends User {
    courses: Course[]
    deadlines: Deadline[]
}

export const useUserStore = defineStore('user', {
    state: (): UserState => ({
        accessToken: '',
        username: '',
        courses: [],
        deadlines: [],
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

        setCourses(courseList: Course[]) {
            this.courses = courseList
        },

        setDeadlines(deadlineList: Deadline[]) {
            this.deadlines = deadlineList
        }
    },
})
