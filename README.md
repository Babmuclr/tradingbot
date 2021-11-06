# tradingbot
外貨ドットコムとOandaから主に、情報をスクレイピングして、データベースを作成しています。

（fintelは表示しているデータが変更になり、情報を得るには、有料会員になる必要があります。 2021/11/06時点）

これらの情報から、1時間後のUSD/JPYなどの通貨の値段を当てることを考えます。一旦、ベースラインとして今回は、ニューラルネットを用いて、モデルを生成しました。そして、その結果を、Twitterにbotとして、30分毎に投稿するようにします。(Twitterアカウント：@prophetFXtrade)

<img width="512" alt="bot" src="https://user-images.githubusercontent.com/44596652/140602856-dad4b4b4-209f-4d8f-9623-c5bba3ba10ee.png">

# 予測モデル
４層のニューラルネットをモデルとして選択した。

- 入力：　外貨ドットコムの20種類の通貨の売買状況と値段、そしてそれらの1時間前との比較
- 出力：標準化された通貨の価格（平均0、分散1）

そして、この出力をもとに、強い買い、弱い買い、変化なし、弱い売り、強い売りを判断します。

# TODO
- 自己回帰モデルであることを考慮する
- 一つ一つの売買の注文の量が重要ではなく、全体としての分布の形が重要であるため、経済の経験則を入れたデータセットへの変更

# 各種HPの状況と取得するデータ
外貨ドットコムの注文状況(https://www.gaitame.com/markets/tool/)

<img width="512" alt="gaika" src="https://user-images.githubusercontent.com/44596652/122717984-51485b80-d2a7-11eb-956b-ac69b76b62bd.png">

OandaのOrderBook(https://widget.oanda.jp/order-book)

<img width="512" alt="oanda" src="https://user-images.githubusercontent.com/44596652/122717991-54dbe280-d2a7-11eb-9258-84f2f8dac990.png">

ETFのショート比率(https://fintel.io/ss/us/)

<img width="512" alt="etf" src="https://user-images.githubusercontent.com/44596652/122717942-4392d600-d2a7-11eb-919e-cf5803eeb89d.png">

から情報をスクレイピングして、機械学習をするためのデータベースを作ることを目的にしています。スクレイピングは、著作権の問題を孕んでいます。あくまで、今回は自分の学習のためにデータを取得しました。

また、学習済みのモデルと現在のデータを用いて、将来のUSD/JPYやEUR/USD、GBP/USD、AUD/USDの値を予測します。

## 外貨ドットコム

外貨ドットコムでは、10分おきに注文情報を載せています。なので、その情報を取得することを考えます。指値や逆指値の注文は、相場の願望が反映されているという前提から、この情報を元に機械学習を行なっていきます。ChromeDriverとSeleniumでスクレイピングをします。urllibとBeautifulSoupではない理由としては、今回取得したいデータは、WEBページ内に図で表されているからです。

## Oanda
Oandaでは、30分おきにオーダーブックとポジションブックを公開しています。Oandaに口座を持っていると、更新の頻度が上がるそうです。Onadapyというのが過去ありましたが、Oandaで口座を解決してかつ取引量が一定数ないと、オーダーブックとポジションブックにアクセスできないようになりました。なので、今回は、外貨ドットコムと同様に、ChromeDriverとSeleniumを用いて、スクレイピングを行います。

## Fintel
Fintelでは、一日ごとに各ETFのポジションを更新しています。一日ごとであるため、スクレイピングをして情報を集める必要はないかもしれません。
