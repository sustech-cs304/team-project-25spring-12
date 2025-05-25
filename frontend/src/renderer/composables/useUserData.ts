import {getCourses} from '../api/course';
import {getDeadlines} from '../api/deadline';
import {useUserStore} from '../store/user';

export async function ensureCoursesLoaded() {
    const store = useUserStore();
    if (!store.courses) {
        const response = await getCourses();
        store.setCourses(response.data);
    }
}

export async function ensureDeadlinesLoaded() {
    const store = useUserStore();
    if (!store.deadlines) {
        const response = await getDeadlines();
        store.setDeadlines(response.data);
    }
}

export async function getRoleByCourseId(courseId: number): Promise<string | null> {
    await ensureCoursesLoaded();
    const store = useUserStore();
    return store.courses?.find(c => c.id === courseId)?.role ?? 'Not Enrolled';
}
