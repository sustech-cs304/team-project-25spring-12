import axios from 'axios'
import humps from 'humps'
import {useUserStore} from "../store/user";

const service = axios.create({
    baseURL: 'http://127.0.0.1:4523/m1/5946426-0-default/', // TODO: baseURL
    timeout: 10000,
})

const userStore = useUserStore();

// 请求前：camelCase 转 snake_case
service.interceptors.request.use(config => {
    const token = userStore.accessToken;
    if (token) {
        config.headers.Authorization = `Bearer ${token}`
        console.log('token added')
    }
    if (config.data) {
        config.data = humps.decamelizeKeys(config.data)
    }
    if (config.params) {
        config.params = humps.decamelizeKeys(config.params)
    }
    console.log(config)
    return config
})

// 响应后：snake_case 转 camelCase
service.interceptors.response.use(
    response => {
        if (response.data) {
            response.data = humps.camelizeKeys(response.data)
        }
        return response
    },
    error => Promise.reject(error)
)

export default service