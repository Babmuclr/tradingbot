# tradingbot

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
