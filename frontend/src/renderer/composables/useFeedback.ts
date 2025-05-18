import {Feedback, FeedbackForm, SubmissionForMark} from "../types/feedback";
import {createFeedbackAttachment, deleteFeedbackAttachment, patchFeedback, postFeedback} from "../api/feedback";
import {uploadFile} from "../api/file";

export function useFeedback() {
    const createFeedback = async (submission: SubmissionForMark, feedbackForm: FeedbackForm, patch: Record<string, Uint8Array>) => {
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
                    const file = new File([patch[attachment.id]], attachment.filename);
                    const formData = new FormData();
                    formData.append("file", file);
                    formData.append("visibility", "public");
                    const response = await uploadFile(formData);
                    const newAttachment = response.data;
                    await createFeedbackAttachment(feedback.id, newAttachment.id);
                    attachments.push(newAttachment);
                } else {
                    await createFeedbackAttachment(feedback.id, attachment.id);
                    attachments.push(attachment);
                }
            }
        }
        feedback.attachments = attachments;
        return feedback;
    };

    const updateFeedback = async (submission: SubmissionForMark, feedbackForm: FeedbackForm, patch: Record<string, Uint8Array>) => {
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
            for (const [attachmentId, blob] of Object.entries(patch)) {
                const selectedAttachment = feedback.attachments.find(attachment => attachment.id === attachmentId);
                if (!selectedAttachment) {
                    console.error(`attachmentId ${attachmentId} not found`);
                    continue;
                }
                const file = new File([blob], selectedAttachment.filename);
                const formData = new FormData();
                formData.append("file", file);
                formData.append("visibility", "public");
                const response = await uploadFile(formData);
                const newAttachment = response.data;
                await deleteFeedbackAttachment(attachmentId);
                await createFeedbackAttachment(feedback.id, newAttachment.id);
                feedback.attachments = feedback.attachments.map(attachment => attachment.id === attachmentId ? attachment: newAttachment);
            }
        }
        return feedback;
    };

    return {
        createFeedback,
        updateFeedback,
    };
}