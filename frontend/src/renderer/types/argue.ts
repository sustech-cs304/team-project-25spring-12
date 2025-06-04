export interface GetArgue {
    assignment: Widget;
    attachments: File[];
    comments: Comment[];
    content: string;
    create_time: string;
    /**
     * 发起人
     */
    editor: Profile;
    /**
     * ID
     */
    id: number;
    not_support: number;
    old_score: number;
    /**
     * =submitted, processed, closed
     */
    status: string;
    submitted_assignment_id: number;
    support: number;
    title: string;
    update_time: string;
    /**
     * 在看
     */
    watch: number;
    widget_id: number;
    [property: string]: any;
}

/**
 * Widget
 */
export interface Widget {
    /**
     * 对应argue的id
     */
    argue_id: number;
    /**
     * document, 或者 assignment 的附件
     */
    attachments?: File[];
    /**
     * 对应 document 的内容
     */
    content?: string;
    create_time: string;
    /**
     * assignment 的 DDL
     */
    ddl?: string;
    editor: Profile;
    /**
     * assignment 的文字反馈
     */
    feedback?: Feedback;
    id: string;
    index: number;
    /**
     * assignment 的总分
     */
    max_score?: number;
    /**
     * notepdf 的笔记
     */
    notes?: Note[];
    /**
     * notepdf / pdf 批改的文件
     */
    pdf_file?: File;
    /**
     * assignment 的分数
     */
    score?: number;
    /**
     * assignment 的状态
     */
    status?: string;
    /**
     * 提交类型file或code
     */
    submit_type?: string;
    /**
     * 如果没交过就是 null
     */
    submitted_assignment: SubmittedAssignment[];
    title: string;
    /**
     * notepdf, doc, assignment
     */
    type: string;
    update_time: string;
    visible: boolean;
    [property: string]: any;
}

/**
 * File
 *
 * notepdf / pdf 批改的文件
 */
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

/**
 * Note
 */
export interface Note {
    editor: Profile;
    id: number;
    page: number;
    text: string;
    x: number;
    y: number;
    [property: string]: any;
}

/**
 * SubmittedAssignment
 */
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

/**
 * Code
 */
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
