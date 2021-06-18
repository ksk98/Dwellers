from views.concrete.view_base import ViewBase
from views.concrete.view_error import ViewError
from views.concrete.view_menu import ViewMenu
from views.concrete.view_settings import ViewSettings
from views.view_enum import Views


class ViewManager:
    """
    A class that manages currently displayed view. Capable of displaying errors on demand.
    """
    def __init__(self):
        # Any views that are created are stored here
        self.__views = {}

        # Initiate some views, start with the menu
        self.reset_views_to_default()
        self.current_view: Views = Views.MENU

        # In case an error is displayed, the view to be displayed next may change on the go.
        self.view_overriden_by_error = False

        self.get_current().clear()
        self.get_current().print_screen()

    def reset_views_to_default(self):
        """
        Initialize the main views used before playing the game.
        """
        self.__views.clear()
        self.__views[Views.MENU] = ViewMenu()
        self.__views[Views.SETTINGS] = ViewSettings()

    def get_current(self) -> ViewBase:
        """
        Get the object of current view.
        """
        return self.__views[self.current_view]

    def has_view_for_enum(self, view: Views) -> bool:
        """
        Check if concrete view was created for specified enum
        :param view:
        :return:
        """
        if self.__views.get(view):
            return True
        return False

    def set_new_view_for_enum(self, view: Views, concrete_view: ViewBase):
        """
        Create a new view object and assign it to an enum. Only one instance per every existing enum is alowed.
        """
        self.__views[view] = concrete_view

    def remove_view_for_enum(self, view: Views):
        """
        Delete a view assigned to a given view enum.
        """
        self.__views[view] = None
        if view == self.current_view:
            self.current_view = Views.MENU

    def set_current(self, view: Views):
        """
        Set enum to be displayed.
        """
        if view is None:
            return

        # Skip the view change if an error was raised. The error may want to overload which view is displayed next.
        if self.view_overriden_by_error:
            self.view_overriden_by_error = False
            return

        # A band-aid fix for always having the first option selected when we enter certain views.
        if view == Views.SETTINGS:
            self.__views[view].selected = 0

        self.current_view = view
        self.get_current().refresh_view()

    def display_error_and_go_to(self, error_message: str, view: Views = Views.MENU):
        """
        Display a new error view and go to a given view after the player presses OK.
        """
        self.__views[Views.ERROR] = ViewError(error_message, view)
        self.current_view = Views.ERROR
        self.view_overriden_by_error = True
        self.get_current().refresh_view()

    def display_error_and_return(self, error_message: str):
        """
        Display a new error view and return to last view after the player presses OK.
        """
        self.display_error_and_go_to(error_message, self.current_view)

    def display_progress(self, progress_view: Views, concrete_view: ViewBase):
        """
        Display a given enum communicating some progress to the player.
        """
        self.__views[progress_view] = concrete_view
        self.current_view = progress_view
        self.get_current().refresh_view()

    def refresh(self):
        """
        Reprint the current view.
        """
        self.get_current().refresh_view()
