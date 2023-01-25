import pandas as pd
import yfinance as yf
import altair as alt
import streamlit as st

st.title('米国株価可視化アプリ')

st.sidebar.write("""
    # GAFA株価
    こちらは株価可視化ツールです。以下のオプションから表示日数を指定してください。
""")

st.sidebar.write("""
    ## 表示日数選択
""")

days = st.sidebar.slider('日数', 1, 50, 20)

st.write(f"""
    ### 過去 **{days}日間**の株価
""")


#キャッシュの利用
@st.cache

#株価を収集する関数を作成
def get_data(days, tickers):
    
    #データを格納するデータフレーム
    df = pd.DataFrame()

    #tickers内の会社リストごとにデータ収集をする
    for company in tickers.keys():

        tkr = yf.Ticker(tickers[company])

        #history()=('~d')は~日分、('max')は取得可能な最大量
        hist = tkr.history(period=f'{days}d')

        #Dateを日、月、年表記に変更
        hist.index = hist.index.strftime('%d %B %Y')

        #データフレームを終値(Close)のみ＋カラム名を会社名に変更
        hist = hist[['Close']]
        hist.columns = [company]

        #行列を入れ替える
        hist = hist.T

        #インデックスの名前をNameへ変更
        hist.index.name = 'Name'

        #データフレームを結合
        df = pd.concat([df, hist])
    return df

try:

    st.sidebar.write("""
        ## 株価の範囲指定
    """)

    ymin, ymax = st.sidebar.slider(
        '範囲を指定してください。',
        0.0, 3500.0, (0.0, 3500.0)
    )


    #会社の指定、会社名はティッカーシンボル
    tickers = {
        'apple': 'AAPL',
        'Meta': 'META',
        'google': 'GOOGL',
        'microsoft': 'MSFT',
        'netflix': 'NFLX',
        'amazon': 'AMZN',
        'TESLA': 'TSLA'
    }

    df = get_data(days, tickers)


    #会社名の選択
    companies = st.multiselect(
        '会社名を選択してください。',
        list(df.index),
        ['google', 'amazon', 'Meta', 'apple']
    )

    #少なくとも一社は選択しなければならないようにする
    if not companies:
        st.error('少なくとも一社は選んでください。')
    else:
        data = df.loc[companies]
        st.write("### 株価（USD）", data.sort_index())
        data = data.T.reset_index()
        #日付、会社名、値の順にする
        #melt:ピボット関数の逆をする
        data = pd.melt(data, id_vars=['Date']).rename(
            columns = {'value': 'Stock Prices(USD)'}
        )
        #線グラフの作成
        chart = (
            alt.Chart(data)
            .mark_line(opacity=0.8, clip=True)
            .encode(
                x = "Date:T",
                y = alt.Y("Stock Prices(USD):Q", stack = None, scale=alt.Scale(domain=[ymin, ymax])),
                color = 'Name:N'
            )
        )      
        #グラフの記述
        st.altair_chart(chart, use_container_width=True)
except:
    st.error(
        "おっと！何かエラーが起きているようです。"
    )