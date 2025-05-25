import request from '../utils/request'
import {Folder} from "../types/folder";

export function getCourses() {
    return request.get('/class')
}

export function getCourse(id: number) {
    return request.get("/class/" + id);
}

export function getFolders(classId: number) {
    return request.get('/class/' + classId + '/folder')
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