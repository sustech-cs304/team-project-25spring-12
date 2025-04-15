import request from '../utils/request'

export async function uploadFile(formData: FormData) {
    return await request.post('/file', formData, {
        headers: {
            'Content-Type': 'multipart/form-data',
        },
    })
}

export async function downloadFile(fileId: string) {
    return request.get('/file/' + fileId, {
        responseType: 'blob',
    })
}