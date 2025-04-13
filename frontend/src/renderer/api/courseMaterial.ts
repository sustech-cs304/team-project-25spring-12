import request from '../utils/request'
import {Note} from "../types/course";

export function getCourseMaterials(id: number) {
    return request.get('/class/page/' + id)
}

export interface NoteCreate extends Note {
    widgetId: number
}

export function createNote(note: Note, widgetId: number) {
    const payload: NoteCreate = {
        ...note,
        widgetId,
    }

    return request.post('/class/widget/notepdf/note', payload)
}