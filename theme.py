#!/usr/bin/env python3

import asyncio
import iterm2

async def main(connection):
    async def update(theme):
        # Themes have space-delimited attributes, one of which will be light or dark.
        parts = theme.split(" ")
        if "dark" in parts:
            preset = await iterm2.ColorPreset.async_get(connection, "one-dark")
        else:
            preset = await iterm2.ColorPreset.async_get(connection, "one-light")

        # Update the list of all profiles and iterate over them.
        profiles=await iterm2.PartialProfile.async_query(connection)
        for partial in profiles:
            # Fetch the full profile and then set the color preset in it.
            profile = await partial.async_get_full_profile()
            await profile.async_set_color_preset(preset)

    app = await iterm2.async_get_app(connection)
    theme = await app.async_get_variable("effectiveTheme")
    await update(theme)

    async with iterm2.VariableMonitor(connection, iterm2.VariableScopes.APP, "effectiveTheme", None) as mon:
        while True:
            # Block until theme changes
            theme = await mon.async_get()
            await update(theme)

iterm2.run_forever(main)
