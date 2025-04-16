import request from '../utils/request';

export const loginApi = (formData: FormData) => {
    return request.post('/user/login', formData, {
        headers: {
            'Content-Type': 'multipart/form-data',
        },
    })
}