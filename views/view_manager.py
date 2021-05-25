from views.concrete.view_base import ViewBase
from views.concrete.view_menu import ViewMenu
from views.concrete.view_lobby import ViewLobby
from views.concrete.view_error import ViewError
from views.view_enum import Views


class ViewManager:
    def __init__(self):
        self.__views = {}
        self.reset_views_to_default()
        self.current_view: Views = Views.MENU

    def reset_views_to_default(self):
        self.__views[Views.MENU] = ViewMenu()
        self.__views[Views.LOBBY] = ViewLobby()

    def get_current(self) -> ViewBase:
        return self.__views[self.current_view]

    def set_new_view_for_enum(self, view: Views, concrete_view: ViewBase):
        self.__views[view] = concrete_view

    def set_current(self, view: Views):
        if view is None:
            return

        self.current_view = view
        self.get_current().refresh_view()

    def display_error(self, error_text: str = "", next_view: Views = Views.MENU):
        self.__views[Views.ERROR] = ViewError(next_view, error_text)
        self.current_view = Views.ERROR
        self.get_current().refresh_view()

    def refresh(self):
        self.get_current().refresh_view()
