import request from '../utils/request'
import type { Note } from '../types/course'

interface NoteCreate extends Note {
    widgetId: number
}

export function createNote(note: Note, widgetId: number) {
    const payload: NoteCreate = {
        ...note,
        widgetId,
    }

    return request.post('/class/widget/notepdf/note', payload)
}
