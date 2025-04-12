import { createRouter, createWebHashHistory, RouteRecordRaw } from 'vue-router';
import Home from '../views/home.vue';
import NProgress from 'nprogress';
import 'nprogress/nprogress.css';

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    redirect: '/course/material?id=123',
    // redirect: '/user-center',  // kl: 之后可以设计一个更适合的默认界面。
  },
  {
    path: '/',
    name: 'Home',
    component: Home,
    children: [
      {
        path: '/user-center',
        name: 'user-center',
        meta: {
          title: '个人中心',
        },
        component: () => import('../views/pages/user-center.vue'),
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
        path: '/argue',
        name: 'argue',
        meta: {
          title: '辩驳',
        },
        component: () => import('../views/pages/argue.vue'),
      },
      {
        path: '/argue_plaza',
        name: 'argue_plaza',
        meta: {
          title: '辩驳广场',
        },
        component: () => import('../views/pages/argue_plaza.vue'),
      },
    ]
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
    path: '/register',
    meta: {
      title: '注册',
      noAuth: true,
    },
    component: () => import('../views/pages/register.vue'),
  },
  {
    path: '/reset-pwd',
    meta: {
      title: '重置密码',
      noAuth: true,
    },
    component: () => import('../views/pages/reset-pwd.vue'),
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
  { path: '/:path(.*)', redirect: '/404' },
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  console.log({to, from, next})
  NProgress.start();
  const role = localStorage.getItem('vuems_name');

  if (!role && to.meta.noAuth !== true) {
    next('/login');
  } else {  // 这里省略了权限检查
    next();
  }
});

router.afterEach(() => {
  NProgress.done();
});

export default router;
