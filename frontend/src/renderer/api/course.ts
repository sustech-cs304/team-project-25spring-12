import request from '../utils/request'
import {Folder} from "../types/folder";

export function getCourses() {
    return request.get('/class')
}

export function getCourseInfo(courseId: number) {
    return request.get('/class/' + courseId)
}

export function getFolders(courseId: number) {
    return request.get('/class/' + courseId + '/folder')
}

interface FolderCreate extends Folder {
    order: number[],  // 包含的所有有序 pageId
    classId: number,
}

export function createFolder(folder: Folder, classId: number) {
    const payload: FolderCreate = {
        ...folder,
        order: [],
        classId,
    }

    return request.post('/class/folder', payload)
}