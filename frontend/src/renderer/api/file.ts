import request from '../utils/request'
import {FileMeta} from "../types/fileMeta";

export async function uploadFile(formData: FormData): Promise<FileMeta> {
    return await request.post('/file', formData, {
        headers: {
            'Content-Type': 'multipart/form-data',
        },
    })
}