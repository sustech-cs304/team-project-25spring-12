export type WidgetType = 'notepdf' | 'doc' | 'assignment';

interface BaseWidget {
    id: string;
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
    attachments?: FileMeta[];
    submitTypes: string[];
    submittedAssignment: SubmittedRecord[] | null;
    status: 'pending' | 'submitted' | 'returned';
    ddl?: string;
    score?: number;
    maxScore?: number;
    feedback?: string;
    argueId?: number;
}

export type WidgetUnion = NotePdfWidget | DocWidget | AssignmentWidget;

/*
* Util interfaces:
* */
export interface FileMeta {
    fileName: string;
    url: string;
}

export interface SubmittedRecord {
    content: string;
    attachments?: FileMeta[];
    code?: { content: string; language: string };
    submittedTime: string;
}

export interface Note {
    id: string;
    page: number;
    x: number;
    y: number;
    text: string;
}

/*
 * End of util interfaces.
 */

import NotePdf from '@/views/widgets/notepdf.vue';
import Doc from '@/views/widgets/doc.vue';
import Assignment from '@/views/widgets/assignment.vue';
import type { WidgetType } from '@/types/widgets';

export const widgetMap: Record<WidgetType, any> = {
    notepdf: NotePdf,
    doc: Doc,
    assignment: Assignment,
};