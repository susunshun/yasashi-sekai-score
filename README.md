# yasashi-sekai-score
あなたのチャンネルが今年一年健全に保たれたか、やさしいせかいだったかをスコアリングします
チャンネルのコメントに、ネガポジ分析を行い、ポジティブであればプラス、ネガティブであればマイナスとして計上しています

## settings
[dotenv](https://pypi.org/project/python-dotenv/) を使用してトークンと解析対象のチャンネルの設定を行います
```
SLACK_TOKEN="your token"
SLACK_CHANNEL_ID="your channel id"
```
