import {FileMeta} from "./fileMeta";
import {Code} from "../api/courseMaterial";

export type WidgetType = 'notepdf' | 'doc' | 'assignment';

export interface BaseWidget {
    id: number;
    type: WidgetType;
    index: number;
    title?: string;
    visible: boolean;
    createTime?: string;
    updateTime?: string;
    editor?: any;
}

export interface NotePdfWidget extends BaseWidget {
    type: 'notepdf';
    pdfFile?: FileMeta;
    notes?: Note[];
}

export interface DocWidget extends BaseWidget {
    type: 'doc';
    content: string;
    attachments?: FileMeta[];
}

export interface Feedback {
    id: number;
    attachments: FileMeta[];
    content: string;
    createTime: string;
    marker: string;
    score: number;
}

export interface Testcase {
    id: number,
    widgetId: number,
    maxCpuTime: number,
    maxMemory: number,
    fileId: string,
}

export interface AssignmentWidget extends BaseWidget {
    type: 'assignment';
    content: string;
    attachments?: FileMeta[];
    submitType: 'file' | 'code';
    submittedAssignment?: SubmittedRecord[];
    status: 'pending' | 'submitted' | 'returned';
    ddl?: string;
    score?: number;
    maxScore: number;
    feedback?: Feedback;
    argueId?: number;
    testCase?: Testcase;
}

export type WidgetUnion = NotePdfWidget | DocWidget | AssignmentWidget;

/*
* Util interfaces:
* */
export interface SubmittedRecord {
    id: number,
    content: string;
    attachments?: FileMeta[];
    code?: Code;
    submittedTime: string;
    feedback?: Feedback;
    student?: any;
}

export interface Note {
    id: number;
    page: number;
    x: number;
    y: number;
    text: string;
}

export function widgetFactory(type: 'doc', index: number): DocWidget
export function widgetFactory(type: 'assignment', index: number): AssignmentWidget
export function widgetFactory(type: 'notepdf', index: number): NotePdfWidget
export function widgetFactory(type: WidgetType, index: number): WidgetUnion {
    const base: Omit<BaseWidget, 'type'> = {
        id: 0,
        index,
        title: '未命名',
        visible: true,
    }

    switch (type) {
        case 'doc':
            return {
                ...base,
                type: 'doc',
                content: '',
                attachments: []
            }
        case 'assignment':
            return {
                ...base,
                type: 'assignment',
                content: '',
                attachments: [],
                submitType: 'file',
                submittedAssignment: [],
                status: 'pending',
                ddl: '',
                maxScore: 100
            }
        case 'notepdf':
            return {
                ...base,
                type: 'notepdf',
                notes: []
            }
        default:
            throw new Error(`Unknown widget type: ${type}`)
    }
}