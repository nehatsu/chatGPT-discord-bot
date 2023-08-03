import os
import openai
import asyncio
import discord
from src.log import logger
from random import randrange
from src.aclient import client
from discord import app_commands
from src import log, art, personas, responses


def run_discord_bot():
    @client.event
    async def on_ready():
        await client.send_start_prompt()
        await client.tree.sync()
        loop = asyncio.get_event_loop()
        loop.create_task(client.process_messages())
        logger.info(f'{client.user} is now running!')


    @client.tree.command(name="chat", description="aiとチャットをする")
    async def chat(interaction: discord.Interaction, *, message: str):
        if client.is_replying_all == "True":
            await interaction.response.defer(ephemeral=False)
            await interaction.followup.send(
                "> **おっと:あなたはすでに replyAll モードになっています。スラッシュコマンドを使いたい場合は、もう一度 `/replyall` を使って通常モードに切り替えてください。**")
            logger.warning("\x1b[31mすでにReplyAllモードになっているので、スラッシュコマンドは使えない！\x1b[0m")
            return
        if interaction.user == client.user:
            return
        username = str(interaction.user)
        client.current_channel = interaction.channel
        logger.info(
            f"\x1b[31m{username}\x1b[0m : /chat [{message}] in ({client.current_channel})")

        await client.enqueue_message(interaction, message)


    @client.tree.command(name="private", description="プライベートモードにする")
    async def private(interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=False)
        if not client.isPrivate:
            client.isPrivate = not client.isPrivate
            logger.warning("\x1b[31mプライベートモードにアクセスした\x1b[0m")
            await interaction.followup.send(
                "> **情報: 次に、プライベート・リプライで応答が送信される。公開モードに戻したい場合は、`/public`**")
        else:
            logger.info("あなたは既にプライベートモードになっています")
            await interaction.followup.send(
                "> **おっと: あなたはすでにプライベート・モードになっています。公開モードに切り替えたい場合は `/public` を使ってください。**")


    @client.tree.command(name="public", description="パブリックモードに切り替える")
    async def public(interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=False)
        if client.isPrivate:
            client.isPrivate = not client.isPrivate
            await interaction.followup.send(
                "> **情報: 次に、レスポンスがチャンネルに直接送信されます。プライベートモードに戻したい場合は `/private` を使ってください。**")
            logger.warning("\x1b[31mSwitch to public mode\x1b[0m")
        else:
            await interaction.followup.send(
                "> **おっと: あなたはすでにパブリック・モードになっています。プライベートモードに切り替えたい場合は `/private` を使ってください。**")
            logger.info("既にパブリックモードになっています")


    @client.tree.command(name="replyall", description="全てのメッセージに反応する")
    async def replyall(interaction: discord.Interaction):
        client.replying_all_discord_channel_id = str(interaction.channel_id)
        await interaction.response.defer(ephemeral=False)
        if client.is_replying_all == "True":
            client.is_replying_all = "False"
            await interaction.followup.send(
                "> **情報: 次に、botはスラッシュコマンドに応答します。replyAll モードに戻したい場合は、もう一度 `/replyAll` を使ってください。**")
            logger.warning("\x1b[31mSwitch to normal mode\x1b[0m")
        elif client.is_replying_all == "False":
            client.is_replying_all = "True"
            await interaction.followup.send(
                "> **情報 : 次に、ボットはスラッシュコマンドを無効にし、このチャンネル内のすべてのメッセージにのみ応答するようにします。通常モードに戻したい場合は、もう一度 `/replyAll` を使ってください。**")
            logger.warning("\x1b[31m replyAll モードに切り替え\x1b[0m")


    @client.tree.command(name="chat-model", description="chatモデルの切り替え")
    @app_commands.choices(choices=[
        app_commands.Choice(name="Official GPT-3.5", value="OFFICIAL"),
        app_commands.Choice(name="Ofiicial GPT-4.0", value="OFFICIAL-GPT4"),
        app_commands.Choice(name="Website ChatGPT-3.5", value="UNOFFICIAL"),
        app_commands.Choice(name="Website ChatGPT-4.0", value="UNOFFICIAL-GPT4"),
        app_commands.Choice(name="Bard", value="Bard"),
        app_commands.Choice(name="Bing", value="Bing"),
    ])

    async def chat_model(interaction: discord.Interaction, choices: app_commands.Choice[str]):
        await interaction.response.defer(ephemeral=False)
        original_chat_model = client.chat_model
        original_openAI_gpt_engine = client.openAI_gpt_engine

        try:
            if choices.value == "OFFICIAL":
                client.openAI_gpt_engine = "gpt-3.5-turbo"
                client.chat_model = "OFFICIAL"
            elif choices.value == "OFFICIAL-GPT4":
                client.openAI_gpt_engine = "gpt-4"
                client.chat_model = "OFFICIAL"
            elif choices.value == "UNOFFICIAL":
                client.openAI_gpt_engine = "gpt-3.5-turbo"
                client.chat_model = "UNOFFICIAL"
            elif choices.value == "UNOFFICIAL-GPT4":
                client.openAI_gpt_engine = "gpt-4"
                client.chat_model = "UNOFFICIAL"
            elif choices.value == "Bard":
                client.chat_model = "Bard"
            elif choices.value == "Bing":
                client.chat_model = "Bing"
            else:
                raise ValueError("無効な選択")

            client.chatbot = client.get_chatbot_model()
            await interaction.followup.send(f"> **情報: あなたは今 {client.chat_model} です.**\n")
            logger.warning(f"\x1b[31 {client.chat_model} model\x1b[0m")

        except Exception as e:
            client.chat_model = original_chat_model
            client.openAI_gpt_engine = original_openAI_gpt_engine
            client.chatbot = client.get_chatbot_model()
            await interaction.followup.send(f"> **エラー: 切り替え中に {choices.value} がエラーを起こしました.**\n")
            logger.exception(f"エラー {choices.value} model: {e}")


    @client.tree.command(name="reset", description="履歴の削除")
    async def reset(interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=False)
        if client.chat_model == "OFFICIAL":
            client.chatbot = client.get_chatbot_model()
        elif client.chat_model == "UNOFFICIAL":
            client.chatbot.reset_chat()
            await client.send_start_prompt()
        elif client.chat_model == "Bard":
            client.chatbot = client.get_chatbot_model()
            await client.send_start_prompt()
        elif client.chat_model == "Bing":
            await client.chatbot.reset()
        await interaction.followup.send("> **情報: 履歴を削除をしました！**")
        personas.current_persona = "standard"
        logger.warning(
            f"\x1b[31m{client.chat_model} は正常にリセットされました\x1b[0m")

 
    @client.tree.command(name="help", description="ヘルプを表示する")
    async def help(interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=False)
        await interaction.followup.send(""":**使い方** \n
        - `/chat [message]` ChatGPTでチャットする！
        - `/draw [prompt]` Dalle2モデルで画像を生成する
        - `/switchpersona [persona]` オプションのchatGPT脱獄を切り替える
                `random`： ランダムにペルソナを選ぶ
                `chatgpt`： 標準のchatGPTモード
                dan`： ダンモード 11.0、悪名高い事ができるモードらそお
                sda`： 優れた DAN がさらに自由になった DAN モード
                コンフィダント`： Evil Confidant（邪悪な腹心の友）、邪悪な腹心の友
                based`：ベースド BasedGPT v2、セクシーGPT
                oppo`： OPPOはchatGPTと正反対のことを言う
                dev`： 開発者モード、v2 開発者モード有効

        - private` ChatGPT をプライベートモードに切り替える。
        - public` ChatGPT をパブリックモードに切り替える。
        - `/replyall` ChatGPT replyAll モードとデフォルトモードの切り替え
        - `/reset` ChatGPTの会話履歴を消去する。
        - `/chat-model` 異なるチャットモデルに切り替える
                OFFICIAL`： GPT-3.5 モデル
                UNOFFICIAL`： ウェブサイトChatGPT
                Bard`： Google Bardモデル

        その他のドキュメントはこちらから:https://github.com/nehatsu/chatGPT-discord-bot/tree/main""")

        logger.info(
            "\x1b[31mSomeone needs help!\x1b[0m")




    @client.tree.command(name="info", description="botの情報")
    async def info(interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=False)
        chat_engine_status = client.openAI_gpt_engine
        chat_model_status = client.chat_model
        if client.chat_model == "UNOFFICIAL":
            chat_model_status = "ChatGPT(UNOFFICIAL)"
        elif client.chat_model == "OFFICIAL":
            chat_model_status = "OpenAI API(OFFICIAL)"
        if client.chat_model != "UNOFFICIAL" and client.chat_model != "OFFICIAL":
            chat_engine_status = "x"
        elif client.openAI_gpt_engine == "テキスト-ダヴィンチ-002-レンダー-シャ":
            chat_engine_status = "gpt-3.5"

        await interaction.followup.send(f"""
```fix
chat-model: {chat_model_status}
gpt-engine: {chat_engine_status}
```
""")


    @client.tree.command(name="draw", description="Dalle2モデルで画像を生成する")
    @app_commands.choices(amount=[
        app_commands.Choice(name="1", value=1),
        app_commands.Choice(name="2", value=2),
        app_commands.Choice(name="3", value=3),
        app_commands.Choice(name="4", value=4),
        app_commands.Choice(name="5", value=5),
        app_commands.Choice(name="6", value=6),
        app_commands.Choice(name="7", value=7),
        app_commands.Choice(name="8", value=8),
        app_commands.Choice(name="9", value=9),
        app_commands.Choice(name="10", value=10),
    ])
    async def draw(interaction: discord.Interaction, *, prompt: str, amount: int = 1):
        if interaction.user == client.user:
            return

        username = str(interaction.user)
        channel = str(interaction.channel)
        logger.info(
            f"\x1b[31m{username}\x1b[0m : /draw [{prompt}] in ({channel})")

        await interaction.response.defer(thinking=True, ephemeral=client.isPrivate)
        try:
            path = await art.draw(prompt, amount)
            files = []
            for idx, img in enumerate(path):
                files.append(discord.File(img, filename=f"image{idx}.png"))
            title = f'> **{prompt}** - {str(interaction.user.mention)} \n\n'

            await interaction.followup.send(files=files, content=title)

        except openai.InvalidRequestError:
            await interaction.followup.send(
                "> **エラー: 不適切な要求 **")
            logger.info(
            f"\x1b[31m{username}\x1b[0m made an inappropriate request.!")

        except Exception as e:
            await interaction.followup.send(
                "> **エラー: 生成できませんでした**")
            logger.exception(f"Error while generating image: {e}")


    @client.tree.command(name="switchpersona", description="オプションのchatGPTジェイルブレイクを切り替える")
    @app_commands.choices(persona=[
        app_commands.Choice(name="Random", value="random"),
        app_commands.Choice(name="Standard", value="standard"),
        app_commands.Choice(name="Do Anything Now 11.0", value="dan"),
        app_commands.Choice(name="Superior Do Anything", value="sda"),
        app_commands.Choice(name="Evil Confidant", value="confidant"),
        app_commands.Choice(name="BasedGPT v2", value="based"),
        app_commands.Choice(name="OPPO", value="oppo"),
        app_commands.Choice(name="Developer Mode v2", value="dev"),
        app_commands.Choice(name="DUDE V3", value="dude_v3"),
        app_commands.Choice(name="AIM", value="aim"),
        app_commands.Choice(name="UCAR", value="ucar"),
        app_commands.Choice(name="Jailbreak", value="jailbreak")
    ])
    async def switchpersona(interaction: discord.Interaction, persona: app_commands.Choice[str]):
        if interaction.user == client.user:
            return

        await interaction.response.defer(thinking=True)
        username = str(interaction.user)
        channel = str(interaction.channel)
        logger.info(
            f"\x1b[31m{username}\x1b[0m : '/switchpersona [{persona.value}]' ({channel})")

        persona = persona.value

        if persona == personas.current_persona:
            await interaction.followup.send(f"> **おっと: すでに`{persona}` になってます**")

        elif persona == "standard":
            if client.chat_model == "OFFICIAL":
                client.chatbot.reset()
            elif client.chat_model == "UNOFFICIAL":
                client.chatbot.reset_chat()
            elif client.chat_model == "Bard":
                client.chatbot = client.get_chatbot_model()
            elif client.chat_model == "Bing":
                client.chatbot = client.get_chatbot_model()

            personas.current_persona = "standard"
            await interaction.followup.send(
                f"> **情報: `{persona}` に切り替えました**")

        elif persona == "random":
            choices = list(personas.PERSONAS.keys())
            choice = randrange(0, 6)
            chosen_persona = choices[choice]
            personas.current_persona = chosen_persona
            await responses.switch_persona(chosen_persona, client)
            await interaction.followup.send(
                f"> **情報: `{chosen_persona}` に切り替えました**")


        elif persona in personas.PERSONAS:
            try:
                await responses.switch_persona(persona, client)
                personas.current_persona = persona
                await interaction.followup.send(
                f"> **情報: `{persona}` に切り替えました**")
            except Exception as e:
                await interaction.followup.send(
                    "> **エラー: 何か問題が発生しました！**")
                logger.exception(f"切り替え時のエラー: {e}")

        else:
            await interaction.followup.send(
                f"> **エラー: アクセス出来ませんでした: `{persona}` 😿**")
            logger.info(
                f'{username} 利用できないペルソナをリクエスト: `{persona}`')


    @client.event
    async def on_message(message):
        if client.is_replying_all == "True":
            if message.author == client.user:
                return
            if client.replying_all_discord_channel_id:
                if message.channel.id == int(client.replying_all_discord_channel_id):
                    username = str(message.author)
                    user_message = str(message.content)
                    client.current_channel = message.channel
                    logger.info(f"\x1b[31m{username}\x1b[0m : '{user_message}' ({client.current_channel})")

                    await client.enqueue_message(message, user_message)
            else:
                logger.exception("replyall`コマンドをもう一度使用してください。")

    TOKEN = os.getenv("DISCORD_BOT_TOKEN")

    client.run(TOKEN)
