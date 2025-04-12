import request from '../utils/request'

export function getCourses() {
    return request.get('/class')
}