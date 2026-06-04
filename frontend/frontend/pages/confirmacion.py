try:
    from components.booking_summary import confirmation
except ModuleNotFoundError:
    from ..components.booking_summary import confirmation

__all__ = ["confirmation"]