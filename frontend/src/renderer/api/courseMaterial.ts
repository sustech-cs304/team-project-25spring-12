import request from '../utils/request'

export function getCourseMaterials(id: number) {
    return request.get('/class/page/' + id)
}

export function postNote()