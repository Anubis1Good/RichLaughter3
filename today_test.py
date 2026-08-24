import os
import pandas as pd
import matplotlib.pyplot as plt
from loaders.ApiMoexLoader import ApiMoexLoader
from datetime import date,timedelta
from utils.work_dfs.convert_tf import convert_timeframe
from traders.VT.bot_on_ticker import bot_on_ticker
from testing.CheckEGTrader import CheckEGTrader
from testing.test_constants import *

today = date.today()
start_date = str(today - timedelta(days=1))
tickers = ['ALRS','ALRS2','MAGN','MAGN2','IRAO','IRAO2','MTLR','MTLR2','RUAL','RUAL2','VTBR','VTBR2','ASTR','ASTR2','ROSN','ROSN2','SBER','SBER2','SIBN','SIBN2','SNGSP','SNGSP2','T','T2','AFLT','AFLT2','HYDR','HYDR2','OGKB','OGKB2','RTKM','RTKM2','TGKA','TGKA2','VKCO','VKCO2']
folder_date = str(today).replace('-','_')
main_folder: str = os.path.join('_test_results/today',folder_date)
os.makedirs(main_folder,exist_ok=True)

for ticker in tickers:
    # loader = ApiMoexLoader(ticker,'RFUD','forts','futures')
    try:
        if '2' in ticker:
            load_ticker = ticker[:-1]
        else:
            load_ticker = ticker
        loader = ApiMoexLoader(load_ticker)
        df = loader.load_data(start_date)
        df = loader.processing_df(df)
        df = convert_timeframe(df,'5min')
        # print(df.head())
        df['ms'] = pd.to_datetime(df['ms'])

        # # 2. Сортируем по времени (на всякий случай)
        df = df.sort_values('ms').reset_index(drop=True)

        # 3. Находим последний день в данных
        last_day = df['ms'].dt.date.max()

        # 4. Отбираем все строки последнего дня
        df_last_day = df[df['ms'].dt.date == last_day]

        # 5. Отбираем строки всех дней, кроме последнего
        df_previous = df[df['ms'].dt.date < last_day]

        # 6. Из предыдущих дней берем последние 80 строк (баров)
        df_previous_last_80 = df_previous.tail(80)

        # 7. Объединяем
        df = pd.concat([df_previous_last_80, df_last_day], ignore_index=True)
        df = df.reset_index(drop=True)
        # print(df.head())
        cwd = CheckEGTrader(
            df,
            bot_on_ticker[ticker],
            MAIN_FEE,
            ticker,
            use_tqdm=True,
            window=80,
            days_mode=DAYS_MODE,
            slip_stop_delta=SLIP_STOP_DELTA)
        
        cwd.check_strategy_window()
        cwd.plot_chart_and_sequtity(show=False)
        img_name = ticker
        full_name_img = os.path.join(main_folder, f"{ticker}.png")
        plt.title(f"{img_name}")
        # plt.legend()
        plt.savefig(full_name_img, bbox_inches='tight')
        plt.close()
    except:
        print(ticker,'не вышло')

