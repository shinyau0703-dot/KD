import pandas as pd, json, os

# 讀取檔案
src=r"D:\Sandy\科定\data-1758877864792.csv"
out=r"D:\Sandy\科定\kd_clean.csv"
df=pd.read_csv(src)

# 展開 json_data
jdf=df["json_data"].dropna().apply(json.loads)
jdf=pd.json_normalize(jdf)

# 攤平成結構化欄位，與原始資料合併
df=pd.concat([df.drop(columns=["json_data"]), jdf], axis=1)

# 嘗試把欄位轉成數值 (失敗就保持原狀)
for c in df.columns:
    df[c]=pd.to_numeric(df[c], errors="ignore")

# 缺失值處理：數值欄位→中位數，其他→眾數
for c in df.columns:
    if df[c].dtype.kind in "biufc":  # 數值型
        df[c]=df[c].fillna(df[c].median())
    else:  # 類別型
        df[c]=df[c].fillna(df[c].mode()[0])

# 輸出乾淨檔
df.to_csv(out,index=False,encoding="utf-8-sig")
print("已輸出:",out," | 形狀:",df.shape)
