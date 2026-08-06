from testing.CheckEGTrader import CheckEGTrader
from strategies.PEGs.PEG1_9 import PEG2_DDCrWork as EG

path_df = '_data_for_tests\data_stock_1m\MTLR_1_1785876346.parquet'
# path_df = '_data_for_tests\data_stock_1m\MTLR_1_1785977685.parquet'
# path_df = '_data_for_tests\data_stock_5m\MTLR_5_1785876346.parquet'
# path_df = '_data_for_tests\data_stock_5m\MTLR_5_1785977685.parquet'
symbol = path_df.split('\\')[-1].split('_')[0]
fee = 0.001
# self.ws = ws[0](self.symbol,self.price_step,1,*ws[1])
ws = [EG,(20,30,20)]
cegt = CheckEGTrader(
    path_df,
    ws,
    fee,
    symbol,
    measure_time=True,
    use_tqdm=True
)

cegt.check_strategy_fast()
cegt.check_strategy_window()
# cegt.check_strategy_fast_debug()
# result_row = cegt.get_statistics()
# print(result_row)

cegt.print_statistics()
cegt.plot_chart_and_sequtity()