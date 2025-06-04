export interface Argue {
    assignment: Widget;
    attachments: File[];
    comments: Comment[];
    content: string;
    create_time: string;
    editor: Profile;
    id: number;
    not_support: number;
    old_score: number;
    status: string;
    submitted_assignment_id: number;
    support: number;
    title: string;
    update_time: string;
    watch: number;
    widget_id: number;
    [property: string]: any;
}

export interface Widget {
    argue_id: number;
    attachments?: File[];
    content?: string;
    create_time: string;
    ddl?: string;
    editor: Profile;
    feedback?: Feedback;
    id: string;
    index: number;
    max_score?: number;
    notes?: Note[];
    pdf_file?: File;
    score?: number;
    status?: string;
    submit_type?: string;
    submitted_assignment: SubmittedAssignment[];
    title: string;
    type: string;
    update_time: string;
    visible: boolean;
    [property: string]: any;
}

export interface File {
    filename: string;
    id: string;
    url: string;
    visibility: string;
    [property: string]: any;
}

/**
 * Profile
 *
 * 发起人
 */
export interface Profile {
    department: string;
    email: string;
    is_active: boolean;
    is_admin: boolean;
    name: string;
    username: string;
    [property: string]: any;
}

/**
 * assignment 的文字反馈
 *
 * Feedback
 */
export interface Feedback {
    attachments?: File[];
    content?: string;
    create_time: string;
    /**
     * ID
     */
    id: string;
    marker?: string;
    score?: number;
    [property: string]: any;
}

export interface Note {
    editor: Profile;
    id: number;
    page: number;
    text: string;
    x: number;
    y: number;
    [property: string]: any;
}

export interface SubmittedAssignment {
    attachments?: File[];
    code?: Code;
    content?: string;
    feedback?: Feedback;
    id: number;
    student?: Profile;
    submitted_time: string;
    [property: string]: any;
}

export interface Code {
    code: string;
    language: string;
    [property: string]: any;
}

export interface Comment {
    content: string;
    create_time: string;
    editor: Profile;
    id: number;
    reply_to: number;
    [property: string]: any;
}
