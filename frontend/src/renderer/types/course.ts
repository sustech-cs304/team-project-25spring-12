export interface Course {
    id: number
    courseCode: string
    name: string
    semester: string
    location: string
    time: string
    lecturer: string
    role: 'student' | 'teacher' | 'teaching assistant'
}