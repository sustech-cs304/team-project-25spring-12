import request from '../utils/request'

export function getDeadlines() {
    return request.get('/ddl')
}