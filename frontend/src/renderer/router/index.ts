import {createRouter, createWebHashHistory, RouteRecordRaw} from 'vue-router'
import Home from '../views/home.vue'
import NProgress from 'nprogress'
import 'nprogress/nprogress.css'
import {useUserStore} from '../store/user'

const routes: RouteRecordRaw[] = [
    {
        path: '/',
        component: Home,
        children: [
            {
                path: '',
                redirect: 'homepage',
            },
            {
                path: 'homepage',
                name: 'homepage',
                meta: {title: '首页'},
                component: () => import('../views/pages/homepage.vue'),
            },
            {
                path: 'course/:courseId/page/:pageId',
                name: 'course-material',
                meta: {title: '课程资料'},
                component: () => import('../views/pages/course-material.vue'),
            },
            {
                path: 'course/:courseId',
                name: 'course',
                meta: {title: '课程'},
                component: () => import('../views/pages/course.vue'),
            },
            {
                path: 'argue',
                name: 'argue-plaza',
                meta: {title: '辩驳广场'},
                component: () => import('../views/pages/argue-plaza.vue'),
            },
            {
                // path: 'argue/:argueId',
                path: 'argue/example',
                name: 'argue-example',
                meta: {title: '辩驳'},
                component: () => import('../views/pages/argue-example.vue'),
            },
            {
                path: 'messages',
                name: 'message-box',
                meta: {title: '消息中心'},
                component: () => import('../views/pages/message-box.vue'),
            },
            {
                path: 'mark/:widgetId',
                name: 'mark',
                meta: {title: '批改'},
                component: () => import('../views/pages/mark.vue'),
            },
        ],
    },
    {
        path: '/login',
        meta: {title: '登录', noAuth: true},
        component: () => import('../views/pages/login.vue'),
    },
    {
        path: '/403',
        meta: {title: '没有权限', noAuth: true},
        component: () => import('../views/pages/403.vue'),
    },
    {
        path: '/404',
        meta: {title: '找不到页面', noAuth: true},
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
    {
        path: '/:path(.*)',
        redirect: '/404',
    },
];


const router = createRouter({
    history: createWebHashHistory(),
    routes,
});

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