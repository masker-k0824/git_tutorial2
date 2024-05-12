import streamlit as st
import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
from datetime import datetime
from matplotlib.colors import rgb2hex

class st_base():
    
    def __init__(self):
        
        self.data_dict ={}
        self.update_time = 0
        self.Ycurve_current = dataimportYcurve()
        
        
    def viewer(self):
        bigin1 = st.sidebar.text_input("日付を入れてください",datetime.today().strftime("%Y-%m-%d"))
        if bigin1 != "" and bigin1 not in self.data_dict:
            self.update_time += 1
            data1 = data_import(bigin1)
            if not data1.dfbs.empty:
                self.data_dict[f"{data1.base_date_str}"] =data1.dfbs
            
        bigin2 = st.sidebar.text_input("日付を入れてください","")
        
        if bigin2 != "" and bigin2 not in self.data_dict:
            self.update_time += 1
            data2 = data_import(bigin2)
            if not data2.dfbs.empty:
                self.data_dict[f"{data2.base_date_str}"] =data2.dfbs
        
        
        selected_option = st.sidebar.selectbox('オプションを選択してください:', self.data_dict.keys(),index = len(self.data_dict.keys())-1)
        st.title(selected_option)
        st.write("売買参考統計値")
        try:
            
            st.dataframe(self.data_dict[f"{selected_option}"])
        except:
            st.write("データなし")
        st.write("国債")
        st.dataframe(self.Ycurve_current.df)
        cmap = plt.get_cmap("jet")
        plt.style.use('fivethirtyeight')
        plt.rcParams['figure.figsize'] = (20, 10)
        fig, axes = plt.subplots()
        plt.rcParams['font.family'] = "MS Gothic"

        for i in self.Ycurve_current.float_col:
            

            axes.plot(self.Ycurve_current.df["基準日"], 
                      self.Ycurve_current.df[i], label = str(i), 
                      color = rgb2hex(cmap(int(i[:-1])*10)), linewidth = 1)

        axes.legend()
        st.pyplot(plt)
        
        
        st.write(self.update_time)
        
    
        
        

class data_import():
    def __init__(self,base_day):
        self.base_date_str = base_day
        self.base_date = datetime.strptime(base_day, "%Y-%m-%d")
        self.BaseHtml = "https://market.jsda.or.jp/shijyo/saiken/baibai/baisanchi/files/"
        self.col = ["日付","銘柄種別","銘柄コード","銘柄名","償還日","利率","平均値複利"
                    ,"平均値単価","平均値単価前日比","利払月","利払日","銘柄属性1","銘柄属性2"
                    ,"銘柄属性3","平均値単利","最高値単価","最高値単利","最低値単価","最低値単利"
                    ,"チェックフラグ","報告者数","最高値複利","最高値単価前日比","最低値複利"
                    ,"最低値単価前日比","中央値複利","中央値単利","中央値単価","中央値単価前日比"]
        
        self.TargetHtml = ""
        self.dfbs = pd.DataFrame()
        self.flag = self.df_setter()
        
    def TargetHtml_Current_setter(self):
        yyyy = self.base_date.strftime("%Y")
        Syymmdd = "S" + self.base_date.strftime("%y%m%d")
        self.TargetHtml = self.BaseHtml + yyyy + "/" + Syymmdd + ".csv"
    
    def TargetHtml_Old_setter(self):
        yyyy = self.base_date.strftime("%Y")
        mm = self.base_date.strftime("%m")
        Syymmdd = "S" + self.base_date.strftime("%y%m%d")
        self.TargetHtml = self.BaseHtml + yyyy + "/" +mm + "/" + Syymmdd + ".csv"
        
        
    def df_reader(self,target_html):
        try:
            df = pd.read_csv(target_html,encoding="SHIFT-JIS",names = self.col)
        except:
            df = pd.read_csv(target_html,encoding="utf_8",names = self.col)
        return df
            
    def df_setter(self):
        
        if self.df_setter_Current():
            #self.df_adjust()
            return True
        elif self.df_setter_Old():
            #self.df_adjust()
            return True
        else:
            self.df = pd.DataFrame()
            return False
    def df_adjust(self):
        self.df["日付"] =pd.to_datetime(self.df["日付"])
        self.df["償還日"] =pd.to_datetime(self.df["償還日"])
        
        
            
            
    def df_setter_Current(self):
        
        try:
            self.TargetHtml_Current_setter()
            self.dfbs = self.df_reader(self.TargetHtml)
            return True
        except:
            return False
        
    def df_setter_Old(self):
        try:
            self.TargetHtml_Old_setter()
            self.dfbs = self.df_reader(self.TargetHtml)
            return True
        except:
            return False
        
    
        
class dataimportYcurve():
    def __init__(self) -> None:
        df_old = pd.read_csv("https://www.mof.go.jp/jgbs/reference/interest_rate/data/jgbcm_all.csv",encoding="SHIFT-JIS", skiprows=1)
        df_cur = pd.read_csv("https://www.mof.go.jp/jgbs/reference/interest_rate/jgbcm.csv",encoding="SHIFT-JIS", skiprows=1)
        self.df = pd.concat([df_old, df_cur])
        self.df["基準日"] = self.df["基準日"].apply(self.wareki_parser)
        self.float_col = list(self.df.columns)[1:]
        self.df.replace('-', float("nan"), inplace=True)
        for i in self.float_col:
            self.df[i] = self.df[i].astype('float')
            
        
        
        
    
    def wareki_parser(self,date_str):
        # 和暦から西暦への変換用辞書
        wareki = {"R": 2018, "H": 1988, "S": 1925}  # 令和、平成、昭和の開始年
        parts = date_str.split(".")

        # 和暦の年月日を整形
        era = str(parts[0][0])
        year = int(parts[0][1:])  + wareki[era] # 年
        month = int(parts[1])     # 月
        day = int(parts[2])       # 日
    
        dt = datetime(year, month, day)
        return dt
    
        

if __name__ == "__main__":
    if 'increment' not in st.session_state: # 初期化
        ins = st_base()
        st.session_state['increment'] = ins
        
        st.session_state['increment'].viewer()
    else:
        st.session_state['increment'].viewer()
    
    
    
    
        
    

        
    
    
    

