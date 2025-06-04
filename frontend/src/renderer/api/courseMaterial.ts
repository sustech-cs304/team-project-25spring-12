import request from '../utils/request'
import {AssignmentWidget, DocWidget, Note, NotePdfWidget, Testcase, WidgetUnion} from "../types/widgets";
import {Page} from "../types/page";

export function getPage(id: number) {
    return request.get('/class/page/' + id)
}

export function createNote(note: Note, widgetId: number) {
    const payload = {
        ...note,
        widgetId,
    }

    return request.post('/class/widget/notepdf/note', payload)
}

export function createPage(page: Page, classId: number, folderId: number) {
    const payload = {
        ...page,
        classId,
        folderId: folderId === 0 ? null : folderId,
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
    code: Code,
}

export function createSubmission(submission: Submission) {
    return request.post('/class/widget/assignment/submit', submission)
}

export function createSubmissionAttachment(submissionId: number, fileId: number) {
    const payload = {
        submissionId,
        fileId
    }

    return request.post('/class/widget/assignment/submit/attach', payload)
}

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
    const uuid = widget.pdfFile.id, payload = {
        ...widget,
        pdfFile: uuid
    }

    return request.post('/class/widget/notepdf', payload)
}

export function editNotePdfWidget(widget: NotePdfWidget, removeNotes: boolean) {
    const uuid = widget.pdfFile.id, payload = {
        ...widget,
        pdfFile: uuid,
        removeNotes
    }

    return request.patch('/class/widget/notepdf', payload)
}

export function createTestcase(testcase: Testcase) {
    const payload: Testcase = {
        ...testcase,
        id: null,
        maxMemory: testcase.maxMemory * 1048576,
    }

    return request.post('/class/widget/testcase', payload);
}

export function editTestcase(testcase: Testcase) {
    const payload: Testcase = {
        ...testcase,
        widgetId: null,
        maxMemory: testcase.maxMemory * 1048576,
    }

    return request.patch('/class/widget/testcase', payload);
}

export function getTestcase(widgetId: number) {
    return request.get('/class/widget/' + widgetId + '/testcase')
}