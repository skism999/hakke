import streamlit as st
import json
import pandas as pd

# メイン関数
def main():
    st.title('暦表示')

    # JSONファイルのパス
    with open('/workspaces/unken/app/data/koyomi/koyomi_daneki.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
        # "koyomi"キーのデータをPandas DataFrameに変換
        df_koyomi = pd.json_normalize(data["koyomi"])

    # 年の選択
    years = df_koyomi['year.value'].unique()
    selected_year = st.selectbox('年を選択してください', years)
    
    # 年のデータをフィルタリング
    df_year = df_koyomi[df_koyomi['year.value'] == selected_year]
    
    if st.button('年のデータを表示'):
        st.write(f'{selected_year}年の一覧:')
        st.dataframe(df_year[['year.value', 'year.jukkan', 'year.junishi',  
                                'month.value', 'month.jukkan', 'month.junishi', 
                                'day.value', 'day.jukkan', 'day.junishi']]) 

    # 年月の選択
    unique_months = df_year['month.value'].unique()
    selected_month = st.selectbox('月を選択してください', unique_months)
    
    # 年月のデータをフィルタリング
    df_month = df_year[df_year['month.value'] == selected_month]

    if st.button('年月のデータを表示'):
        st.write(f'{selected_year}年{selected_month}月の一覧:')
        st.dataframe(df_month[['year.value', 'year.jukkan', 'year.junishi',  
                                'month.value', 'month.jukkan', 'month.junishi', 
                                'day.value', 'day.jukkan', 'day.junishi']])     
    
    # 年月日の選択
    unique_days = df_month['day.value'].unique()
    selected_day = st.selectbox('日を選択してください', unique_days)
    
    # 年月日のデータをフィルタリング
    df_day = df_month[df_month['day.value'] == selected_day]

    if st.button('年月日のデータを表示'):
        st.write(f'{selected_year}年{selected_month}月{selected_day}日のデータ:')
        st.dataframe(df_day[['year.value', 'year.jukkan', 'year.junishi',  
                                'month.value', 'month.jukkan', 'month.junishi', 
                                'day.value', 'day.jukkan', 'day.junishi']]) 

if __name__ == '__main__':
    main()
