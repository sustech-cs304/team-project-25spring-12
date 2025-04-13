import request from '../utils/request'
import {Folder} from "../types/folder";

export function getCourses() {
    return request.get('/class')
}

export function getFolders(classId: number) {
    return request.get('/class/' + classId + '/folder')
}

interface FolderCreate extends Folder {
    order: number[],  // 包含的所有有序 pageId
}

export function createFolder(folder: Folder) {
    const payload: FolderCreate = {
        ...folder,
        [],
    }

    return request.post('/class/folder', payload)
}