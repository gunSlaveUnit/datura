from PySide6.QtCore import QObject, Signal, Property, Slot


class NavigationLogic(QObject):
    """
    Provides functionality to track the indexes
    of the store pages that the user navigates while working
    """

    current_page_changed = Signal()
    current_index_changed = Signal()
    current_history_length_changed = Signal()

    def __init__(self):
        super().__init__()

        self._pages_history = [0]
        self._current_index = 0
        self._current_history_length = len(self._pages_history)

    @Slot(int)
    def add(self, added_index: int):
        if self._pages_history[-1] != added_index:
            self._pages_history.append(added_index)

            self._current_index = len(self._pages_history) - 1
            self.current_index_changed.emit()
            self.current_page_changed.emit()

            self._current_history_length += 1
            self.current_history_length_changed.emit()

    @Slot(int)
    def remove(self, removed_index: int):
        if removed_index in self._pages_history:
            self._pages_history.remove(removed_index)

            self._current_index = len(self._pages_history) - 1
            self.current_index_changed.emit()
            self.current_page_changed.emit()

            self._current_history_length -= 1
            self.current_history_length_changed.emit()

    @Slot()
    def clear(self):
        self._pages_history = [0]

        self.current_index = 0
        self.current_page = self._pages_history[self._current_index]
        self.current_history_length = len(self._pages_history)

        self.current_index_changed.emit()
        self.current_page_changed.emit()
        self.current_history_length_changed.emit()

    @Slot()
    def back(self):
        if self._current_index > 0:
            self._current_index -= 1
            self.current_index_changed.emit()
            self.current_page_changed.emit()

    @Slot()
    def forward(self):
        if self._current_index < self._current_history_length - 1:
            self._current_index += 1
            self.current_index_changed.emit()
            self.current_page_changed.emit()

    current_page = Property(int,
                            lambda self: self._pages_history[self._current_index],
                            lambda self, value: None,
                            notify=current_page_changed)

    current_index = Property(int,
                             lambda self: self._current_index,
                             lambda self, value: setattr(self, '_current_index', value),
                             notify=current_index_changed)

    current_history_length = Property(int,
                                      lambda self: self._current_history_length,
                                      lambda self, value: setattr(self, '_current_history_length', value),
                                      notify=current_history_length_changed)
