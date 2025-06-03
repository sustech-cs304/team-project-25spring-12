import request from '../utils/request'
import {AssignmentWidget, DocWidget, Note, NotePdfWidget, WidgetUnion} from "../types/widgets";
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

export function createSubmission() {}

export function addWidgetAttachment(widgetId: number, fileId: string) {
    const payload = {
        widgetId: widgetId,
        fileId: fileId,
    }

    return request.post('/class/widget/attachment', payload)
}

export function removeWidgetAttachment(fileId: string) {
    return request.delete('/class/widget/attachment/' + fileId)
}

export function createAssignmentWidget(widget: AssignmentWidget) {
    return request.post('/class/widget/assignment', widget)
}

export function editAssignmentWidget(widget: AssignmentWidget) {
    return request.patch('/class/widget/assignment', widget)
}

export function createDocWidget(widget: DocWidget) {
    return request.post('/class/widget/doc', widget)
}

export function editDocWidget(widget: DocWidget) {
    return request.patch('/class/widget/doc', widget)
}

export function createNotePdfWidget(widget: NotePdfWidget) {
    return request.post('/class/widget/notepdf', widget)
}

export function editNotePdfWidget(widget: NotePdfWidget) {
    return request.patch('/class/widget/notepdf', widget)
}