import {FileMeta} from "./fileMeta";

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
    feedback?: string;
    argueId?: number;
}

export type WidgetUnion = NotePdfWidget | DocWidget | AssignmentWidget;

/*
* Util interfaces:
* */
export interface SubmittedRecord {
    content: string;
    attachments?: FileMeta[];
    code?: { content: string; language: string };
    submittedTime: string;
}

export interface Note {
    id: number;
    page: number;
    x: number;
    y: number;
    text: string;
}