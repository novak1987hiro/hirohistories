import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image #画像の挿入
import time

#タイトルの追加
st.title('Streamlit 超入門')

#テキストの追加
st.write('DataFrame')

#データフレームの作成
df = pd.DataFrame(
    np.random.rand(100,2),
    columns=['lat','lon']
)
    

#表を表示させる
#静的な表の場合はst.table(df)、動的な表の場合はst.dataframe(df)
#st.write(df)でも可能だが表を操作するなら下記
#style.highlight_max():最大値を目立たせる
st.dataframe(df.style.highlight_max(axis=0), width=300, height=300)


#マジックコマンド
"""
# 章
## 節
### 項

'''python
import streamlit as st
import numpy as np
import pandas as pd
'''
"""

#折線グラフでプロット
st.line_chart(df)
#line_chart:普通の折線グラフ
#area_chart:折線グラフの塗り潰し
#bar_chart:棒グラフ


#マップのプロット
#新宿付近のプロット
df_map = pd.DataFrame(
    np.random.rand(100,2)/[50,50] + [35.69, 139.70],
    columns=['lat','lon']
)
st.map(df_map)


#画像の挿入
st.write('Display Image')
img = Image.open('IMG_0041.JPG')
#use_column_width=True：アプリのカラム幅に合わせる
st.image(img, caption='Kusatsu', use_column_width=True)


#st.checkbox():チェックボックス
st.write('Display Image')
if st.checkbox('Show Image'):
    img = Image.open('IMG_0041.JPG')
    st.image(img, caption='Kusatsu', use_column_width=True)


#st.selectbox():選択肢
option = st.selectbox(
    'あなたが好きな数字を教えてください。',
    list(range(1,11))
)
'あなたの好きな数字は、',option,'です。'


#text_input:テキスト入力
st.write('Interactive Widgets')
text = st.text_input('あなたの趣味を教えてください。')
'あなたの趣味は、',text,'です。'


#st.slider('言葉',最小値,最大値,デフォルトの値):スライド式で選択できるやつ
condition = st.slider('あなたの今の調子は？', 0, 100, 50)
'コンディション：',condition


#サイドバー
st.sidebar.write('Sidebar')
text_sidebar = st.sidebar.text_input('あなたの趣味は？')
condition_sidebar = st.sidebar.slider('あなたの調子は？', 0, 100, 50)
'あなたの趣味は、',text_sidebar,'です。'
'コンディション：',condition_sidebar


#2カラムレイアウト
st.write('Two column')
left_column, right_column = st.columns(2)
button = left_column.button('右カラムに文字を表示')
if button:
    right_column.write('ここは右カラム')


#expandar＝押すと開くやつ
expandar = st.expander('問い合わせ')
expandar.write('問い合わせ内容を書く')


#プログレスバー
st.write('プログレスバーの表示')
'Start!!'
latest_iteration = st.empty()
bar = st.progress(0)
for i in range(100):
    latest_iteration.text(f'Iteration {i+1}')
    bar.progress(i + 1)
    time.sleep(0.1)
'Done!!!!!!'