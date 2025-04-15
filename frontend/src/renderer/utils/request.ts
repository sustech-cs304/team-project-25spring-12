import axios from 'axios'
import humps from 'humps'
import {useUserStore} from "../store/user";

const service = axios.create({
    baseURL: '10.16.165.147:8001/api/v1/',
    timeout: 10000,
})

let userStore = null;

function initUserStore() {
    userStore = useUserStore();
}

// 请求前：camelCase 转 snake_case
service.interceptors.request.use(config => {
    if (!userStore) initUserStore()
    const token = userStore.accessToken;
    if (token) {
        config.headers.Authorization = `Bearer ${token}`
    }
    if (config.data) {
        config.data = humps.decamelizeKeys(config.data)
    }
    if (config.params) {
        config.params = humps.decamelizeKeys(config.params)
    }
    return config
})

// 响应后：snake_case 转 camelCase
service.interceptors.response.use(response => {
        if (response.data) {
            response.data = humps.camelizeKeys(response.data)
        }
        return response
    },
    error => Promise.reject(error)
)

export default service