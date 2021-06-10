from views.concrete.view_base import ViewBase
from views.concrete.view_menu import ViewMenu
from views.concrete.view_error import ViewError
from views.view_enum import Views


class ViewManager:
    def __init__(self):
        self.__views = {}
        self.reset_views_to_default()
        self.current_view: Views = Views.MENU

    def reset_views_to_default(self):
        self.__views[Views.MENU] = ViewMenu()

    def get_current(self) -> ViewBase:
        return self.__views[self.current_view]

    def set_new_view_for_enum(self, view: Views, concrete_view: ViewBase):
        self.__views[view] = concrete_view

    def remove_view_for_enum(self, view: Views):
        self.__views[view] = None

    def set_current(self, view: Views):
        if view is None:
            return

        if self.current_view == Views.ERROR:
            self.current_view = self.get_current().get_view_for_selected()
        else:
            self.current_view = view

        self.get_current().refresh_view()

    def display_error(self, concrete_view: ViewBase):
        self.__views[Views.ERROR] = concrete_view
        self.current_view = Views.ERROR
        self.get_current().refresh_view()

    def display_progress(self, progress_view: Views, concrete_view: ViewBase):
        self.__views[progress_view] = concrete_view
        self.current_view = progress_view
        self.get_current().refresh_view()
