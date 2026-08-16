from testing.CheckEGTrader import CheckEGTrader
from strategies.PEGs.PEG1_9 import PEG2_DDCrWork as EG
# from strategies.PEGs.PEG10_19 import PEG11_KUSURUKEN as EG
# from strategies.PEGs.PEG20_29 import PEG26_UNKNOWN as EG
# from strategies.LEGs.LEG1 import LEG1_BIBI as EG
# from strategies.LEGs.LEG2 import LEG2_DRG as EG
# from strategies.WEGs.WEG1_9 import WEG3_DS as EG
# from strategies.UEGs.UEG1_9 import UEG9_GRAVY as EG
# from strategies.UEGs.UEG1_9 import UEG7_PIGEON as EG
# from strategies.SEGs.SEG_CA1_9 import SEG1_LITE as EG
# from strategies.SEGs.SEG_ML10_19 import SEGML2b_RAPTOR as EG
# from strategies.VEGs.VEG1 import VEG1_VENUS as EG

path_df = '_data_for_tests\\before_opt\MTLR_5_1786793053.parquet'
# path_df = '_data_for_tests\data_stock_1m\MTLR_1_1785977685.parquet'
# path_df = '_data_for_tests\data_stock_5m\MTLR_5_1785876346.parquet'
# path_df = '_data_for_tests\data_stock_5m\MTLR_5_1785977685.parquet'
symbol = path_df.split('\\')[-1].split('_')[0]
fee = 0.001
ws = [EG,[]]
# ws = [EG,(100,30,20)]
# ws = [UEG4_FALCON,],

# ws = [EG,(33,22,53,2.9,0.8,22,)]
cegt = CheckEGTrader(
    path_df,
    ws,
    fee,
    symbol,
    measure_time=True,
    use_tqdm=True
)

# cegt.check_strategy_fast()
# cegt.print_statistics()
cegt.check_strategy_faster()
cegt.print_statistics()
cegt.check_strategy_window()
# cegt.check_strategy_fast_debug()
# result_row = cegt.get_statistics()
# print(result_row)

cegt.print_statistics()
# cegt.plot_chart_and_sequtity()
# cegt.plot_chart_and_sequtity(help_info='sltp')