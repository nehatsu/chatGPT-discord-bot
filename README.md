# ChatGPT Discord Bot

> ### ChatGPTを使ってDiscordボットを作ろう
> このbotはChatGPT Discord Botを日本語翻訳したものです。

---
> **Warning**
>
> #### 2023-04-12 Bing をサポートしました
> #### 2023-03-27 Bard をサポートしました
> #### 2023-08-02 非公式GPT-4は現在ダウン中（多分使えない状態）

### Chat

![image](https://user-images.githubusercontent.com/89479282/206497774-47d960cd-1aeb-4fba-9af5-1f9d6ff41f00.gif)

# セットアップ

## インストールするために必要なもの

* タスクマネージャーで実行してください ```pip3 install -r requirements.txt```

* **`.env.example` のファイルの名前を `.env`に変更してください**

* 推奨のpythonのバージョンは `3.9` 以上です。
---
## ステップ 1: discord botの作り方

1. https://discord.com/developers/applications にアクセスします
2. アプリケーションでDiscordボットを作成する
3. ボット設定からトークンをコピー

   ![image](https://user-images.githubusercontent.com/89479282/205949161-4b508c6d-19a7-49b6-b8ed-7525ddbef430.png)
4. `コピーしたトークンを.env`の `DISCORD_BOT_TOKEN`にペースト

   <img height="190" width="390" alt="image" src="https://user-images.githubusercontent.com/89479282/222661803-a7537ca7-88ae-4e66-9bec-384f3e83e6bd.png">

5. discord デベロッパーパネル内の MESSAGE CONTENT INTENT `をonにして下さい`

   ![image](https://user-images.githubusercontent.com/89479282/205949323-4354bd7d-9bb9-4f4b-a87e-deb9933a89b5.png)

6. discord デベロッパーパネル内の OAuth2 URL Generatorでurlを作成その際Application Commandとbotにチェックを入れておいて下さい

   ![image](https://user-images.githubusercontent.com/89479282/205949600-0c7ddb40-7e82-47a0-b59a-b089f929d177.png)
---
> **Note**
>
> ステップ2では、使用したいモデルの認証プロセスのみを完了させる必要があります（ステップ2すべてを完了させる必要はありません）。
>
> .env`ファイルで`CHAT_MODEL`を使用したいデフォルトモデルに変更することを忘れないこと。

## ステップ 2: open ai API keyを作成する 

### OpenAI API keyが作成できるサイトに飛びます
1.  https://beta.openai.com/account/api-keys

2. 飛んだらCreate new secret keyをおす

   ![image](https://user-images.githubusercontent.com/89479282/207970699-2e0cb671-8636-4e27-b1f3-b75d6db9b57e.PNG)

3. discrdのトークンと同じように`.env` の `OPENAI_API_KEY`にコピペする

---
## Step 2: Web版の ChatGPTのやり方

> **重要 Plus Accountのユーザーのみ有効**

1.  https://chat.openai.com/api/auth/session を開く

2. `F12`を押す。

3.  `Application` tab > Cookiesの順に開く

   ![image](https://user-images.githubusercontent.com/89479282/229298001-41ab4f61-5b79-4c65-b08c-708ee6fe2304.png)

4. クッキーから`_puid`の値をコピーし、`.env`の`PUID`の下に貼り付ける。

5. クッキーから `accessToken` の値をコピーし、`.env` の `ACCESS_TOKEN` の下に貼り付ける。

---
## ステップ 2: Google Bard のやり方
1. bardのサイトに飛びます://bard.google.com/

2. `F12`をおす

3. `Application` tab > Cookiesの順に開く

4. クッキーから `__Secure-1PSID` の値をコピーし、`.env` の `BARD_SESSION_ID` の下に貼り付ける。

---
## ステップ 2: Microsoft Bing のやり方
1. **ファイル `cookies.dev.json` を `cookies.json` に名前を変える。**

2. Go to https://bing.com/chat and log in your Microsoft account

3. Use Cookie Editor or similar extensions to export the cookies

4. Paste it into `cookies.json`

---
## ステップ 3: デスクトップ上でbotを起動しよう！

1. ターミナルかコマンドプロントを開きます

2. ChatGPT Discordボットをインストールしたディレクトリに移動する。

3. `python3 main.py` か`python main.py` を入力しbotを実行させます。
---
## ステップ 3: Dockerを使ったbotの起動の仕方

1. Dockerイメージをビルドし、Dockerコンテナ`docker compose up -d`を実行する。

2. ボットがうまく動作しているかどうかを次で調べる `docker logs -t chatgpt-discord-bot`

   ### botの止め方:

* 実行中のサービスのリストを見るには `docker ps` を実行する。
* 実行中のボットを停止するには `docker stop <ボットコンテナID>` を実行する。

### それではよいchat gptを～
---

## オプション: 自動ログイン
>  * 自動ログイン機能により、ボットは提供された認証情報を使用してGoogle BardまたはMicrosoft Bingに自動的にログインします。
>  * 必要なクッキーを自動的に取得します。

*  この機能を有効にするには、まず`.env`ファイルの`chrome_version`フィールドにクロームブラウザのバージョンを入力してください。
*google bard
   1. .env` の `bard_enable_auto_login` を `True` に設定する。
   2. .env`に`google_account`と`google_password`を記入する。

      (注意:  自動ログインが機能するのは、2faを持っていないgoogleアカウントだけです。)
* Microsoft Bing
   1. .env` で `bing_enable_auto_login` を `True` に設定する。
   2. 次に `.env` に `bing_account` と `bing_password` を入力する。

## オプション: Setup system prompt

* ボットの初回起動時またはリセット時に、システムプロンプトが表示される。
* system_prompt.txt`の内容を修正することで設定できる。
* ファイル内のテキストはすべて、ボットへのプロンプトとして実行される。
* DiscordチャンネルでChatGPTbotからの最初のメッセージを受け取る！
* Discordの設定で「開発者モード」をオンにする

   1. メッセージを受信したいチャンネルを右クリックし、`コピーID`をクリックする。

        ![channel-id](https://user-images.githubusercontent.com/89479282/207697217-e03357b3-3b3d-44d0-b880-163217ed4a49.PNG)

   2. これを `.env` の `DISCORD_CHANNEL_ID` の下に貼り付ける。

## おまけ2: ロギングを無効化する

* .env`の`LOGGING`の値をFalseに設定する。

------
>  [**中文設置教學**](https://zero6992.me/2023/03/08/chatGPT-discord-bot-chinese/)
------
## botのコマンド

* `/chat [message]` ChatGPTでチャットする！
* `/draw [prompt]` Dalle2モデルで画像を生成する
* `/switchpersona [persona]` オプションのchatGPT脱獄を切り替える
   * `random`： ランダムにペルソナを選ぶ
   * `chatGPT`： 標準のchatGPTモード
   * `dan`： ダンモード 11.0、悪名高い何でもモード
   * `sda`： Superior DAN は DAN モードでさらに自由度が増しました。
   * コンフィダント Evil Confidant（イービル・コンフィダント）：邪悪な信頼できる腹心の部下。
   * `based`： BasedGPT v2、セクシーな gpt
   * `oppo`: OPPO： OPPOはchatGPTと正反対のことを言う
   * `dev`： 開発者モード、v2 開発者モード有効

* `/private` ChatGPTをプライベートモードに切り替える。
* `/public` ChatGPT をパブリックモードに切り替える
* `/replyall` ChatGPT replyAll モードとデフォルトモードの切り替え
* `/reset` ChatGPTの会話履歴を消去する。
* `/chat-model` 異なるチャットモデルに切り替える
   * `official-gpt-3.5`： GPT-3.5 モデル
   * `official-gpt-4.0`： GPT-4.0 モデル (アカウントが gpt-4 モデルにアクセスできることを確認してください)
   * ウェブサイトChatGPT-3.5`： ウェブサイト ChatGPT-3.5 モデル (UNOFFICIAL)
   * ウェブサイト ChatGPT-4.0`： ウェブサイトChatGPT-4.0モデル(UNOFFICIAL)(プラスアカウントを持っていれば利用可能)
   * Bard`： Google Bardモデル
   * Bing`： Microsoft Bingモデル


### 特別な機能

#### 描く

![image](https://user-images.githubusercontent.com/91911303/223772051-13f840d5-99ef-4762-98d2-d15ce23cbbd5.png)

#### ペルソナのスイッチ
> **注意**
>
> 特定のペルソナを使用すると、下品なコンテンツや不穏なコンテンツが生成される可能性があります。自己責任でご利用ください。


![image](https://user-images.githubusercontent.com/91911303/223772334-7aece61f-ead7-4119-bcd4-7274979c4702.png)


#### モード

* パブリックモード (デフォルト) ` ボットが直接チャンネルに返信する。

  ![image](https://user-images.githubusercontent.com/89479282/206565977-d7c5d405-fdb4-4202-bbdd-715b7c8e8415.gif)

* プライベートモード`の場合、ボットの返事はコマンドを使った本人しか見ることができない。

  ![image](https://user-images.githubusercontent.com/89479282/206565873-b181e600-e793-4a94-a978-47f806b986da.gif)

* replyallモード` ボットはスラッシュコマンドを使わずにチャンネル内のすべてのメッセージに返信します (`/chat` も利用できなくなります)

   > **注意**
   > ボットは簡単に `replyall` モードでトリガーされ、プログラムの失敗を引き起こす可能性があります。(つまりなんのメッセージでも反応するから、botの反応がバグる可能性があるということ)
 ---
