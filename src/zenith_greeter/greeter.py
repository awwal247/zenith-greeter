"""Greeting utilities for Python applications."""


class Greeter:
    """Build consistent greetings with optional custom wording.

    Args:
        name: Person to greet. Empty or whitespace-only names become ``"there"``.
        greeting: Opening word or phrase, such as ``"Hello"`` or ``"Welcome"``.
        welcome_message: Optional message appended after the greeting.

    Example:
        >>> Greeter("Awwal").greet()
        'Hello, Awwal! Welcome to Python packages.'
        >>> Greeter("Ada", greeting="Hi", welcome_message="Good to see you.").greet()
        'Hi, Ada! Good to see you.'
    """

    def __init__(
        self,
        name: str = "there",
        greeting: str = "Hello",
        welcome_message: str = "Welcome to Python packages.",
    ) -> None:
        if not isinstance(name, str):
            raise TypeError("name must be a string")
        if not isinstance(greeting, str):
            raise TypeError("greeting must be a string")
        if not isinstance(welcome_message, str):
            raise TypeError("welcome_message must be a string")

        greeting = greeting.strip()
        if not greeting:
            raise ValueError("greeting cannot be empty")

        self.name = name.strip() or "there"
        self.greeting = greeting
        self.welcome_message = welcome_message.strip()

    def greet(self) -> str:
        """Return the configured greeting as a string."""
        message = f"{self.greeting}, {self.name}!"
        if self.welcome_message:
            message += f" {self.welcome_message}"
        return message
