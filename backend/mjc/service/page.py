from fastapi import HTTPException, status
from sqlmodel import Session

import mjc.service.assignment
from mjc.model.schema.common import Message
from mjc.model.schema.page import Page, PageCreate, PageUpdate
from mjc.model.schema.user import UserInDB
from mjc.model.schema.widget import AssignmentWidget, NotePdfWidget, DocWidget
from mjc.model.entity.page import Page as PageEntity
from mjc.model.entity.widget import WidgetType
from mjc.model.entity.course import ClassRole
from mjc.crud import page as crud_page
from mjc.service import widget as widget_service, course as course_service, assignment as assignment_service


def entity2page(entity: PageEntity) -> Page:
    page = Page(id=entity.id,
                name=entity.name,
                index=entity.index,
                visible=entity.visible,
                widgets=[widget_service.entity2widget(widget) for widget in entity.widgets if widget and widget.is_deleted == False])
    return page


def get_page(db: Session, page_id: int, current_user: UserInDB) -> Page | None:
    page = crud_page.get_page(db, page_id)
    if not page:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Page not found")
    role = course_service.get_user_class_role(db, current_user.username, page.class_id)
    widgets: list[AssignmentWidget | NotePdfWidget | DocWidget] = []
    for widget in page.widgets:
        if not widget.is_deleted:
            if widget.type == WidgetType.assignment:
                if role == ClassRole.STUDENT:
                    widgets.append(assignment_service.get_student_submissions(db, widget, current_user.username))
                elif role == ClassRole.TEACHER or role == ClassRole.TA or current_user.is_admin:
                    widgets.append(widget_service.entity2assignment(widget))
            elif widget.type == WidgetType.note_pdf:
                widgets.append(widget_service.entity2notepdf(widget))
            elif widget.type == WidgetType.doc:
                widgets.append(widget_service.entity2doc(widget))
    page = Page(id=page.id,
                name=page.name,
                index=page.index,
                visible=page.visible,
                widgets=widgets)
    return page


def create_page(db: Session, page_create: PageCreate) -> Page :
    page = crud_page.create_page(db, page_create)
    if not page:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Create page failed")
    return entity2page(page)


def update_page(db: Session, page_update: PageUpdate) -> Page:
    page = crud_page.update_page(db, page_update)
    if not page:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Update page failed")
    return entity2page(page)


def delete_page(db: Session, page_id: int) -> Message:
    page = crud_page.delete_page(db, page_id)
    if page:
        return Message(msg="Page deleted successfully")
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Delete page failed")
