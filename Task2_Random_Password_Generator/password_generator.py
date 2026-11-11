"""Generate strong random passwords from selected character groups."""

from __future__ import annotations

import argparse
import secrets
import string


def generate_password(
    length: int = 16,
    *,
    lowercase: bool = True,
    uppercase: bool = True,
    digits: bool = True,
    symbols: bool = True,
) -> str:
    """Create a password with at least one character from each enabled group."""
    groups: list[str] = []
    if lowercase:
        groups.append(string.ascii_lowercase)
    if uppercase:
        groups.append(string.ascii_uppercase)
    if digits:
        groups.append(string.digits)
    if symbols:
        groups.append(string.punctuation)

    if not groups:
        raise ValueError("Enable at least one character group.")
    if not isinstance(length, int) or isinstance(length, bool):
        raise ValueError("Length must be an integer.")
    if length < len(groups):
        raise ValueError(
            f"Length must be at least {len(groups)} for the enabled groups."
        )

    all_characters = "".join(groups)
    password_characters = [secrets.choice(group) for group in groups]
    password_characters.extend(
        secrets.choice(all_characters) for _ in range(length - len(groups))
    )
    secrets.SystemRandom().shuffle(password_characters)
    return "".join(password_characters)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate a random password using Python's secrets module."
    )
    parser.add_argument(
        "-l",
        "--length",
        type=int,
        default=16,
        help="password length (default: 16)",
    )
    parser.add_argument(
        "--no-lowercase",
        action="store_true",
        help="exclude lowercase letters",
    )
    parser.add_argument(
        "--no-uppercase",
        action="store_true",
        help="exclude uppercase letters",
    )
    parser.add_argument(
        "--no-digits",
        action="store_true",
        help="exclude digits",
    )
    parser.add_argument(
        "--no-symbols",
        action="store_true",
        help="exclude punctuation symbols",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        password = generate_password(
            length=args.length,
            lowercase=not args.no_lowercase,
            uppercase=not args.no_uppercase,
            digits=not args.no_digits,
            symbols=not args.no_symbols,
        )
    except ValueError as exc:
        print(f"Error: {exc}")
        return 2

    print(password)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
