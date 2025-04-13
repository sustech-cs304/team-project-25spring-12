import request from '../utils/request'

export function getCourses() {
    return request.get('/class')
}

export function getFolders(classId: number) {
    return request.get('/class/' + classId + '/folder')
}