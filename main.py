import sys
from typing import Final

import aiohttp
import discord
import flet as ft

LOCALE_NAMES: Final[dict[discord.Locale, str]] = {
    discord.Locale.american_english: "English",
    discord.Locale.taiwan_chinese: "繁體中文",
    discord.Locale.chinese: "简体中文",
    discord.Locale.indonesian: "Bahasa Indonesia",
    discord.Locale.dutch: "Nederlands",
    discord.Locale.french: "Français",
    discord.Locale.japanese: "日本語",
    discord.Locale.brazil_portuguese: "Português (Brasil)",
}
NAME_TO_LOCALE: Final[dict[str, discord.Locale]] = {
    v: k for k, v in LOCALE_NAMES.items()
}


async def fetch_commands(locale: discord.Locale) -> dict[str, str]:
    async with aiohttp.ClientSession() as session, session.get(
        "https://hb-api.seriaati.xyz/commands", params={"locale": locale.value}
    ) as response:
        data = await response.json()
        return data


def popup_menu_item_on_click(e: ft.ControlEvent) -> None:
    e.page.launch_url(e.control.data)


def add_command_cards(page: ft.Page, commands: dict[str, str]) -> None:
    cards: list[ft.Card] = []
    for name, desc in commands.items():
        cards.append(
            ft.Card(
                content=ft.Container(
                    content=ft.ListTile(
                        title=ft.Text(name),
                        subtitle=ft.Text(desc),
                    ),
                    width=400,
                    padding=10,
                ),
                height=130,
            )
        )
    page.add(ft.Row(cards, wrap=True, spacing=10))


async def change_locale_on_click(e: ft.ControlEvent) -> None:
    locale = NAME_TO_LOCALE[e.control.value]
    commands = await fetch_commands(locale)
    e.page.clean()
    e.page.add(
        ft.Container(
            ft.Dropdown(
                options=[
                    ft.dropdown.Option(text=name, data=locale.value)
                    for locale, name in LOCALE_NAMES.items()
                ],
                value=LOCALE_NAMES[locale],
                label="Language",
                on_change=change_locale_on_click,
                width=400,
            ),
            padding=ft.padding.only(top=10),
        )
    )
    add_command_cards(e.page, commands)
    e.page.update()


async def main(page: ft.Page) -> None:
    locale = discord.Locale.american_english
    commands = await fetch_commands(locale)

    page.title = "Hoyo Buddy Commands"
    page.scroll = ft.ScrollMode.ADAPTIVE
    page.appbar = ft.AppBar(
        title=ft.Container(
            ft.Text("Hoyo Buddy Commands", size=20),
            margin=ft.margin.symmetric(vertical=10),
        ),
        actions=[
            ft.PopupMenuButton(
                items=[
                    ft.PopupMenuItem(
                        icon=ft.icons.WEB_OUTLINED,
                        text="Official website",
                        data="https://seria.is-a.dev/hoyo-buddy/",
                        on_click=popup_menu_item_on_click,
                    ),
                    ft.PopupMenuItem(
                        icon=ft.icons.CODE_OUTLINED,
                        text="Source code",
                        data="https://github.com/seriaati/hoyo-buddy",
                        on_click=popup_menu_item_on_click,
                    ),
                    ft.PopupMenuItem(
                        icon=ft.icons.START_OUTLINED,
                        text="Get started",
                        data="https://github.com/seriaati/hoyo-buddy/wiki/Getting-Started",
                        on_click=popup_menu_item_on_click,
                    ),
                ]
            ),
        ],
        toolbar_height=64,
    )
    page.add(
        ft.Container(
            ft.Dropdown(
                options=[
                    ft.dropdown.Option(text=name, data=locale.value)
                    for locale, name in LOCALE_NAMES.items()
                ],
                value=LOCALE_NAMES[locale],
                label="Language",
                on_change=change_locale_on_click,
                width=400,
            ),
            padding=ft.padding.only(top=10),
        )
    )

    add_command_cards(page, commands)


ft.app(
    main, view=None if sys.platform == "linux" else ft.AppView.WEB_BROWSER, port=4563
)
