# yasashi-sekai-score
あなたのチャンネルが今年一年健全に保たれたか、やさしいせかいだったかをスコアリングします
Channelのコメントに対してネガポジ分析を掛けて、ポジティブであればプラス、ネガティブであればマイナスとして計上しています

## settings
[dotenv](https://pypi.org/project/python-dotenv/) を使用してトークンと解析対象のチャンネルの設定を行います
このリポジトリのルートに `.env` ファイルを作成してください

```
# .env
SLACK_TOKEN="your token"
SLACK_CHANNEL_ID="your channel id"
```
