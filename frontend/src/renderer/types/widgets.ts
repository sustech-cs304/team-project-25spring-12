import {FileMeta} from "./fileMeta";
import {Code} from "../api/courseMaterial";

export type WidgetType = 'notepdf' | 'doc' | 'assignment';

export interface BaseWidget {
    id: number;
    type: WidgetType;
    index: number;
    title?: string;
    visible: boolean;
    createTime: string;
    updateTime: string;
    editor?: any;
}

export interface NotePdfWidget extends BaseWidget {
    type: 'notepdf';
    pdfFile: FileMeta;
    notes: Note[];
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

export interface AssignmentWidget extends BaseWidget {
    type: 'assignment';
    content: string;
    attachments: FileMeta[];
    submitType: 'file' | 'code';
    submittedAssignment: SubmittedRecord[] | null;
    status: 'pending' | 'submitted' | 'returned';
    ddl: string;
    score: number;
    maxScore: number;
    feedback?: Feedback;
    argueId?: number;
}

export type WidgetUnion = NotePdfWidget | DocWidget | AssignmentWidget;

/*
* Util interfaces:
* */
export interface SubmittedRecord {
    id: number,
    content?: string;
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