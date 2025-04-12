export interface Course {
    id: string
    courseCode: string
    name: string
    semester: string
    location: string
    time: string
    lecturer: string
    role: 'student' | 'teacher' | 'ta'
}