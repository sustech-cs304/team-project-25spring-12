import {SubmittedRecord} from "@/types/widgets";

export interface FeedbackForm {
    score?: number;
    content?: string;
}

export interface Grades {
    id: number;
    widgetId: number;
    title: string;
    submitType: 'file' | 'code';
    content?: string;
    maxScore?: number;
    createTime?: string;
    updateTime?: string;
    submissions: SubmittedRecord[];
}
