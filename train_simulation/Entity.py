from abc import ABC, abstractproperty

class Entity(ABC):
    @abstractproperty
    def image(self):
        pass

    def get_figure(self):
        return self.image
