import request from '../utils/request'
import {Note, WidgetUnion} from "../types/widgets";
import {Page} from "../types/page";

export function getPage(id: number) {
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

interface pageCreate extends Page {
    classId: number,
    folderId: number,
}

export function createPage(page: Page, classId: number, folderId: number) {
    const payload: pageCreate = {
        ...page,
        classId,
        folderId,
    }

    return request.post('/class/page', payload)
}

export function createWidget(widget: WidgetUnion) {
    return request.post('/class/widget/' + widget.type, widget)
}

export interface Code {
    code: string,
    language: string,
}

export interface Submission {
    widgetId: number,
    content: string,
    attachments: File[],
    code: Code,
}

export function createSubmission()