import {createRouter, createWebHashHistory, RouteRecordRaw} from 'vue-router'
import Home from '../views/home.vue'
import NProgress from 'nprogress'
import 'nprogress/nprogress.css'
import {useUserStore} from '../store/user'

const routes: RouteRecordRaw[] = [
    {
        path: '/',
        redirect: '/homepage',
    },
    {
        path: '/',
        name: 'Home',
        component: Home,
        children: [
            {
                path: '/homepage',
                name: 'homepage',
                meta: {
                    title: '首页',
                },
                component: () => import('../views/pages/homepage.vue'),
            },
            {
                path: '/course/material',
                name: 'course-material',
                meta: {
                    title: '课程信息',
                },
                component: () => import('../views/pages/course-material.vue'),
            },
            {
                path: '/messages',
                name: 'message-box',
                meta: {
                    title: '消息中心',
                },
                component: () => import('../views/pages/message-box.vue'),
            },
        ],
    },
    {
        path: '/login',
        meta: {
            title: '登录',
            noAuth: true,
        },
        component: () => import('../views/pages/login.vue'),
    },
    {
        path: '/403',
        meta: {
            title: '没有权限',
            noAuth: true,
        },
        component: () => import('../views/pages/403.vue'),
    },
    {
        path: '/404',
        meta: {
            title: '找不到页面',
            noAuth: true,
        },
        component: () => import('../views/pages/404.vue'),
    },
    {
        path: '/401',
        meta: {
            title: '登录状态失效',
            noAuth: true,
        },
        component: () => import('../views/pages/401.vue'),
    },
    {path: '/:path(.*)', redirect: '/404'},
]

const router = createRouter({
    history: createWebHashHistory(),
    routes,
})

router.beforeEach((to, from, next) => {
    NProgress.start()

    const userStore = useUserStore()
    userStore.loadTokenFromStorage()

    const isLoggedIn = !!userStore.accessToken
    const noAuth = to.meta.noAuth === true

    if (!isLoggedIn && !noAuth) {
        next('/401')
    } else {
        next()
    }
})

router.afterEach(() => {
    NProgress.done()
})

export default router