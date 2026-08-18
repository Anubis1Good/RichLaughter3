from testing.CheckEGTrader import CheckEGTrader
from strategies.all_egs import *
from strategies.helpEGs.debugEG import DebugAction,DebugMean

# path_df = '_data_for_tests\\before_opt\MTLR_5_1786793053.parquet'
path_df = '_data_for_tests\_before_opt\ALRS_5_1786793061.parquet'
# path_df = '_data_for_tests\data_stock_5m\MTLR_5_1785876346.parquet'
# path_df = '_data_for_tests\data_stock_5m\MTLR_5_1785977685.parquet'
symbol = path_df.split('\\')[-1].split('_')[0]
fee = 0.001
window = 60
# window = 110
# ws = [EG,[]]
# ws = [EG,(100,30,20)]
# ws = [UEG4_FALCON,],

# ws = (PEG14_RENEGADE,(5,35,39,29,45,10,40,57,))
ws = (PEG16_LEORIC,[])
# ws = (DebugMean,[])
cegt = CheckEGTrader(
    path_df,
    ws,
    fee,
    symbol,
    measure_time=True,
    use_tqdm=True,
    window=window
)
cegt.df = cegt.df.iloc[-500:]
# cegt.check_strategy_fast()
# cegt.print_statistics()
cegt.check_strategy_faster()
# cegt.ws.save_to_csv("faster_actions.csv")
# cegt.ws.save_to_csv("faster_means.csv")
cegt.print_statistics()
# cegt.plot_chart_and_sequtity()
# cegt.ws.debug_data = []
cegt.check_strategy_window(normalization=False)
# cegt.ws.save_to_csv("window_actions.csv")
# cegt.ws.save_to_csv("window_means.csv")
# cegt.check_strategy_fast_debug()
# result_row = cegt.get_statistics()
# print(result_row)

cegt.print_statistics()
# cegt.plot_chart_and_sequtity()
# cegt.plot_chart_and_sequtity(help_info='sltp')