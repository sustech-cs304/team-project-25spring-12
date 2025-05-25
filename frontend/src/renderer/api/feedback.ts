import request from "../utils/request";

export function getAllSubmissions(widgetId: number) {
    return request.get("/class/widget/" + widgetId + "/submission");
}

interface FeedbackCreate {
    score?: number;
    content?: string;
    submissionId: number;
}

export function postFeedback(payload: FeedbackCreate) {
    return request.post("/class/widget/assignment/feedback", payload);
}

interface FeedbackPatch {
    submissionId: number;
    score: number;
    content: string;
    id: number;
}

export function patchFeedback(payload: FeedbackPatch) {
    return request.patch("/class/widget/assignment/feedback", payload);
}

export function createFeedbackAttachment(feedbackId: number, fileId: string) {
    const payload = {feedbackId, fileId};
    return request.post("/class/widget/assignment/feedback/attach", payload);
}

export function deleteFeedbackAttachment(fileId: string) {
    return request.delete("/class/widget/assignment/feedback/attach/" + fileId);
}
