from testing.CheckEGTrader import CheckEGTrader
from strategies.all_egs import *
from strategies.helpEGs.debugEG import DebugAction,DebugMean
from testing.test_constants import *


# PATH_DF = '_data_for_tests\data_stock_5m\AFLT_5_1790444114.parquet'
symbol = PATH_DF.split('\\')[-1].split('_')[0]
# fee = 0.001
# window = 60
# window = 110
# window = 200
# ws = [EG,[]]
# ws = [EG,(100,30,20)]
# ws = [UEG4_FALCON,],

# ws = (SEG1_LITE,(None,108,70,0.7,0.7,57),9,None) #проверить! 0 сделок в окне!
ws = (SEG1_LITE,(None,108,70,0.7,0.7,57),9,None) #проверить! 0 сделок в окне!
# ws = (PEG30_ETC2,[])
# ws = (UEG7_LOVERDUCK,[])
# ws = (DebugMean,[])
cegt = CheckEGTrader(
    PATH_DF,
    ws,
    MAIN_FEE,
    symbol,
    measure_time=True,
    use_tqdm=True,
    window=WINDOW,
    days_mode=DAYS_MODE,
    slip_stop_delta=SLIP_STOP_DELTA
)
# cegt.df = cegt.df.iloc[-500:]
# cegt.check_strategy_fast()
# cegt.print_statistics()
# cegt.check_strategy_faster()
cegt.check_strategy_faster(debug=True)
# cegt.ws.save_to_csv("faster_actions.csv")
# cegt.ws.save_to_csv("faster_means.csv")
cegt.print_statistics()
# cegt.plot_chart_and_sequtity()
ef_fast = cegt.trade_data['step_eq_fee']

cegt.plot_chart_and_sequtity()
# cegt.ws.debug_data = []
cegt.check_strategy_window(normalization=True)
# cegt.check_strategy_window(normalization=False)
# ef_window = cegt.trade_data['step_eq_fee']
# cegt.ws.save_to_csv("window_actions.csv")
# cegt.ws.save_to_csv("window_means.csv")
# cegt.check_strategy_fast_debug()
# result_row = cegt.get_statistics()
# print(result_row)

cegt.print_statistics()
# cegt.plot_chart_and_sequtity()
# import matplotlib.pyplot as plt

# full_name_img = os.path.join(images_folder, f"{name_file}.png")
# name_bot = 'Vasya'
# plt.figure(figsize=(12, 6))
# plt.plot(ef_window, color='red', label='Equity')
# plt.plot(ef_fast, color='blue', label='Equity with Fees')
# plt.show()
# plt.title(f"{name_bot}")
# plt.legend()
# plt.savefig(full_name_img, bbox_inches='tight')
# plt.close()