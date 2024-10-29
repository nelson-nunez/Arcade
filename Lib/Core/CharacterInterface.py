from abc import ABC, abstractmethod
import pygame

class CharacterInterface(ABC):
    @abstractmethod
    def mover(self):
        pass

    @abstractmethod
    def derrota(self):
        pass

    @abstractmethod
    def dibujar(self, surface: pygame.Surface):
        pass

    @abstractmethod
    def destruir(self, surface: pygame.Surface):
        pass
