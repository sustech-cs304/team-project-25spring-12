import {getCourses} from '../api/course';
import {getDeadlines} from '../api/deadline';
import {useUserStore} from '../store/user';

export async function ensureCoursesLoaded() {
    const store = useUserStore();
    if (!store.courses) {
        const {data} = await getCourses();
        store.setCourses(data);
    }
}

export async function ensureDeadlinesLoaded() {
    const store = useUserStore();
    if (!store.deadlines) {
        const {data} = await getDeadlines();
        store.setDeadlines(data);
    }
}

export async function getRoleByCourseId(courseId: number): Promise<string | null> {
    const store = useUserStore();
    if (!store.courses) {
        const {data} = await getCourses();
        store.setCourses(data);
    }
    return store.courses?.find(c => c.id === courseId)?.role ?? null;
}
