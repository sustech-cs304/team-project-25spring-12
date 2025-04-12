export interface ClassItem {
    id: number;
    name: string;
    courseCode: string;
    semester: string;
    lecturer: string;
    location: string;
    time: string;
    role?: 'student' | 'teacher' | 'ta' | string;
}

