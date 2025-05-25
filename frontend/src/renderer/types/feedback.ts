import {FileMeta} from "./fileMeta";
import {Code} from "@/api/courseMaterial";

interface Profile {
    username: string;
    name: string;
    department: string;
    email: string;
}

export interface SubmissionForMark {
    id: number;
    content?: string;
    attachments?: FileMeta[];
    code?: Code;
    submittedTime: string;
    feedback?: Feedback;
    student?: Profile;
}

export interface Feedback {
    id: number;
    score?: number;
    content?: string;
    attachments?: FileMeta[];
    createTime: string;
    marker?: string;
}

export interface FeedbackForm {
    score?: number;
    content?: string;
}
