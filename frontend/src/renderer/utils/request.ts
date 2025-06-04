import axios from 'axios'
import humps from 'humps'
import {useUserStore} from "../store/user";
import router from '../router/index';
import {ElMessage} from "element-plus";

const service = axios.create({
    baseURL: 'http://10.16.165.147/api/v1/',
    // baseURL: 'http://127.0.0.1:4523/m1/5946426-5634400-default',
    timeout: 10000,
})

const userStore = useUserStore();

// 请求前：camelCase 转 snake_case
service.interceptors.request.use(config => {
    const token = userStore.accessToken;
    if (token) {
        config.headers.Authorization = `Bearer ${token}`
    }
    if (config.data && typeof config.data === 'object' && !(config.data instanceof FormData)) {
        config.data = humps.decamelizeKeys(config.data)
    }
    if (config.params) {
        config.params = humps.decamelizeKeys(config.params)
    }
    return config
})

// 响应后：snake_case 转 camelCase
service.interceptors.response.use(
    response => {
        const contentType = response.headers['content-type'] || '';
        if (contentType.includes('application/json') && typeof response.data === 'object') {
            response.data = humps.camelizeKeys(response.data)
        }
        return response;
    },
    error => {
        const { response, config } = error;

        if (response) {
            const requestUrl = config.url || '';

            switch (response.status) {
                case 401:
                    if (requestUrl.includes('/user/login')) {
                        // Nothing
                        // 登录时提供了错误的账号密码
                    } else {
                        // 未登录或 token 过期
                        ElMessage.error('登录状态已失效，请重新登录');
                        router.push('/login');
                    }
                    break;

                case 500:
                    ElMessage.error('服务器错误，请稍后重试');
                    break;

                default:
                    ElMessage.error(response.data?.message || '请求出错');
            }
        } else {
            ElMessage.error('网络错误或请求超时');
        }

        return Promise.reject(error);
    }
);

export default service