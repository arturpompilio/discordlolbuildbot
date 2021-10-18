import discord
from discord.ext import commands
from discord.utils import get
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import os
import time
import random

intents = discord.Intents.default()
intents.members = True

testing = False

client = commands.Bot(command_prefix = "++", case_insensitive = True, intents=intents)

client.remove_command('help')

options = webdriver.ChromeOptions()
options.headless = True
driver = webdriver.Chrome(ChromeDriverManager().install(), options = options)
#driver.implicitly_wait(10)

@client.command()
@commands.cooldown(1, 10, commands.BucketType.default)
async def build(ctx,campeao,lane='None'):
    async with ctx.typing():
        if lane == "None":
            driver.get(f'https://br.op.gg/champion/{campeao}')
        else:
            driver.get(f'https://br.op.gg/champion/{campeao}/statistics/{lane}/build')
            if driver.current_url != f'https://br.op.gg/champion/{campeao}/statistics/{lane}/build' and driver.current_url != "https://br.op.gg/champion/statistics":
                link_dividido = driver.current_url.split("/")
                await ctx.send(f"{ctx.author.mention}, eu não achei a lane **{lane}**, procurando builds para **{link_dividido[6].capitalize()}** (mais popular)...")

        if driver.current_url == "https://br.op.gg/champion/statistics":
            await ctx.send(f"{ctx.author.mention}, eu não achei o campeão **{campeao}** por esse nome, tente novamente tudo junto e sem caracteres especiais.")
        else:
            S = lambda X: driver.execute_script('return document.body.parentNode.scroll'+X)
            driver.set_window_size(S("Width"),S("Height"))
            telas=driver.find_elements_by_class_name(f'champion-overview__table')#.screenshot("skillabilities.png")
            for tela in telas:
                tela.screenshot("build.png")
                await ctx.send(file=discord.File('build.png'))

    driver.Dispose()

@client.command()
@commands.cooldown(1, 10, commands.BucketType.default)
async def counter(ctx,campeao,lane="None"):
    async with ctx.typing():
        if lane == "None":
            driver.get(f'https://br.op.gg/champion/{campeao}')
        else:
            driver.get(f'https://br.op.gg/champion/{campeao}/statistics/{lane}/build')
            if driver.current_url != f'https://br.op.gg/champion/{campeao}/statistics/{lane}/build' and driver.current_url != "https://br.op.gg/champion/statistics":
                link_dividido = driver.current_url.split("/")
                await ctx.send(f"{ctx.author.mention}, eu não achei a lane **{lane}**, procurando builds para **{link_dividido[6].capitalize()}** (mais popular)...")
            
        if driver.current_url == "https://br.op.gg/champion/statistics":
            await ctx.send(f"{ctx.author.mention}, eu não achei o campeão **{campeao}** por esse nome, tente novamente tudo junto e sem caracteres especiais.")
        else:
            S = lambda X: driver.execute_script('return document.body.parentNode.scroll'+X)
            driver.set_window_size(S("Width"),S("Height"))
            telas=driver.find_elements_by_css_selector(f'td.champion-stats-header-matchup__table__champion')#.screenshot("skillabilities.png")
            await ctx.send(f"Esses campeões são **bons contra** {campeao.capitalize()}:")
            for tela in telas:
                tela.screenshot(f"counter.png")
                await ctx.send(file=discord.File(f'counter.png'))

    driver.Dispose()


@build.error
async def build_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"{ctx.author.mention}, aguarde mais **{error.retry_after:.2f}s**")

@counter.error
async def counter_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"{ctx.author.mention}, aguarde mais **{error.retry_after:.2f}s**")



client.run('')