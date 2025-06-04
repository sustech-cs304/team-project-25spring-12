import {FeedbackForm} from "../types/feedback";
import {createFeedbackAttachment, deleteFeedbackAttachment, patchFeedback, postFeedback} from "../api/feedback";
import {uploadFile} from "../api/file";
import {FileMeta} from "../types/fileMeta";
import {Feedback, SubmittedRecord} from "../types/widgets";

export function useFeedback() {
    const createFeedback = async (submission: SubmittedRecord, feedbackForm: FeedbackForm, patch: Record<string, Promise<Uint8Array>>) => {
        const payload = {
            score: feedbackForm.score,
            content: feedbackForm.content,
            submissionId: submission.id,
        };
        const response = await postFeedback(payload);
        const feedback = response.data as Feedback;
        const attachments = [];
        if (submission.attachments) {
            for (const attachment of submission.attachments) {
                if (attachment.id in patch) {
                    const file = new File([await patch[attachment.id]], attachment.filename);
                    const formData = new FormData();
                    formData.append("file", file);
                    formData.append("visibility", "public");
                    const response = await uploadFile(formData);
                    const newAttachment = response.data as FileMeta;
                    await createFeedbackAttachment(feedback.id, newAttachment.id);
                    attachments.push(newAttachment);
                    delete patch[attachment.id];
                } else {
                    await createFeedbackAttachment(feedback.id, attachment.id);
                    attachments.push(attachment);
                }
            }
        }
        feedback.attachments = attachments;
        return feedback;
    };

    const updateFeedback = async (submission: SubmittedRecord, feedbackForm: FeedbackForm, patch: Record<string, Promise<Uint8Array>>) => {
        if (!submission.feedback) {
            console.error(`no feedback found in submission ${submission.id}`);
            return;
        }
        if (feedbackForm.score === undefined || feedbackForm.content === undefined) {
            console.error(`score or content is undefined`);
            return;
        }
        const payload = {
            submissionId: submission.id,
            score: feedbackForm.score,
            content: feedbackForm.content,
            id: submission.feedback.id,
        };
        const response = await patchFeedback(payload);
        const feedback = response.data as Feedback;
        if (feedback.attachments !== undefined) {
            const attachments = [];
            for (const attachment of feedback.attachments) {
                if (attachment.id in patch) {
                    const file = new File([await patch[attachment.id]], attachment.filename);
                    const formData = new FormData();
                    formData.append("file", file);
                    formData.append("visibility", "public");
                    const response = await uploadFile(formData);
                    const newAttachment = response.data as FileMeta;
                    await deleteFeedbackAttachment(attachment.id);
                    await createFeedbackAttachment(feedback.id, newAttachment.id);
                    attachments.push(newAttachment);
                    delete patch[attachment.id];
                } else {
                    attachments.push(attachment);
                }
            }
            feedback.attachments = attachments;
        }
        return feedback;
    };

    return {
        createFeedback,
        updateFeedback,
    };
}
