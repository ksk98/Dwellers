from views.concrete.view_base import ViewBase
from views.concrete.view_menu import ViewMenu
from views.concrete.view_error import ViewError
from views.concrete.view_settings import ViewSettings
from views.view_enum import Views


class ViewManager:
    def __init__(self):
        self.__views = {}
        self.reset_views_to_default()
        self.current_view: Views = Views.MENU
        self.view_overriden_by_error = False

    def reset_views_to_default(self):
        self.__views[Views.MENU] = ViewMenu()
        self.__views[Views.SETTINGS] = ViewSettings()

    def get_current(self) -> ViewBase:
        return self.__views[self.current_view]

    def set_new_view_for_enum(self, view: Views, concrete_view: ViewBase):
        self.__views[view] = concrete_view

    def remove_view_for_enum(self, view: Views):
        self.__views[view] = None

    def set_current(self, view: Views):
        if view is None:
            return

        if self.view_overriden_by_error:
            self.view_overriden_by_error = False
            return

        if view == Views.SETTINGS:
            self.__views[view].selected = 0

        self.current_view = view

        self.get_current().refresh_view()

    def display_error_and_go_to(self, error_message: str, view: Views = Views.MENU):
        self.__views[Views.ERROR] = ViewError(error_message, view)
        self.current_view = Views.ERROR
        self.view_overriden_by_error = True
        self.get_current().refresh_view()

    def display_error_and_return(self, error_message: str):
        self.display_error_and_go_to(error_message, self.current_view)

    def display_progress(self, progress_view: Views, concrete_view: ViewBase):
        self.__views[progress_view] = concrete_view
        self.current_view = progress_view
        self.get_current().refresh_view()

    def refresh(self):
        self.get_current().refresh_view()
