import { defineStore } from 'pinia'
import type {User} from '../types/user'
import type {Course} from '../types/course'
import type {Deadline} from "../types/deadline";
import {getCourses} from "../api/course";
import {getDeadlines} from "../api/deadline";

interface UserState extends User {
    courses: Course[] | null
    deadlines: Deadline[] | null
}

export const useUserStore = defineStore('user', {
    state: (): UserState => ({
        accessToken: '',
        username: '',
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
        },

        async getCourses(): Promise<Course[]> {
            if (this.courses === null) {
                const response = await getCourses()
                this.courses = response.data as Course[]
            }
            return this.courses
        },

        async getDeadlines(): Promise<Deadline[]> {
            if (this.deadlines === null) {
                const response = await getDeadlines()
                this.deadlines = response.data as Deadline[]
            }
            return this.deadlines
        },

        async getRoleByCourseId(courseId: number): Promise<string> {
            if (this.courses === null) {
                const response = await getCourses()
                this.courses = response.data as Course[]
            }
            return this.courses.find(c => c.id == courseId)?.role ?? null
        }
    },
})
