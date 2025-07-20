import inspect
import pandas as pd
from proj_consts import paths
import logging
"""
# symbols=["^GSPC","AAPL","KO","PEP","NESN","ADM"]#,"NFLX","MSFT"]
#aus checked: "VUG","VOOG","ASX","QOZ.XA","A200.AX","BEAR.AX","BBOZ.AX"
aus resources checked: "FAIR.AX","QRE.AX","ACDC.AX","QRE.AX","OZXX.AX","OZR.AX"]
aus best ["JZRO.AX","ACDC.AX"]
aus materials ["GBND.AX","XMET.AX","PAVE.AX"]
aus fundamentally sound ["BHP.AX","AX1.AX","CBA.AX","CSL.AX","WES.AX","WDS.AX",
         "WDS.AX","WOW.AX","RIO.AX","ALL.AX","WTC.AX","STO.AX","COL.AX",
         "JBH.AX","ARB.AX","DTL.AX","CLV.AX","LAU.AX","GRR.AX"]

aus gold ["NST.AX","NST.AX","SFR.AX","CMM.AX","GOR.AX"]
"PDN.AX","BOE.AX","ERA.AX","PEN.AX","AGE.AX"


Gold etf "^XAU","GLDN.AX","GLD"
iShares "IAF.AX","BILL.AX","IWLD.AX","ITEK.AX","IOZ.AX"
        "EMXC.AX","IEM.AX","IHEB.AX","IZZ.AX", "IGRO.AX","IBAL.AX"
        "ILB.AX","IJP.AX","IAA.AX","IVV.AX","IOO.AX" ,"IXI.AX"   
Chances: "IGRO.AX","IBAL.AX" ,"IXI.AX"   
#"BTC-USD" PROBLEM
"""
TA_INDICES = True

class defs:
    def __init__(self,ui_choices: dict) -> None:
        if ui_choices:
            self.durations = ui_choices["durations"]
            self.symbols = ui_choices["symbols"]
            self.lst_wthrwl = ui_choices["lst_wthrwl"]
            self.fin_tools = ui_choices["fin_tools"]
            self.start = ui_choices["start"]
            self.end = ui_choices["end"]
        else:
            self.durations=range(1,4)#[3,5,10,15]#,3,4,5]#[3,7,14]#,5,10]#[3,5,10,15]#years
            self.symbols=["^GSPC"]#["IGRO.AX","IBAL.AX" ,"IXI.AX" ,"VGS.AX",
                    #"^GSPC","GBTC","TA35.TA"]

            #self.symbols=from_definition()
            self.lst_wthrwl=0#days#Years Ago #TODO: make use
            self.fin_tools=["yfinance","ta_indices","more_indices"]# gemel,yfinance,ta_indices
            self.start = None
            self.end = None

        self.report=False
        self.logger = set_logger()

def stock_symbols_tabler():
    definitions_file = paths.definitions
    table = pd.read_excel(definitions_file,sheet_name="StockSymbols")
    return table

def from_definition():
    symbols = stock_symbols_tabler()
    bol_DataSource = symbols["DataSource"].apply(lambda x: x=="yfinance").to_list()
    bol=pd.DataFrame(bol_DataSource,symbols["Analyze"]).reset_index()
    bol=bol.all(axis='columns').to_list()
    return symbols.loc[bol,"Symbol"].drop_duplicates().to_list()

def set_logger():
    """
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR,
    'critical': logging.CRITICAL
    """
    my_logger = logging.getLogger('my-logger')
    my_logger.handlers.clear()

    my_logger.setLevel(logging.INFO)
    fmt = '[%(levelname)s] %(asctime)s - %(message)s'
    log_formatter_a = logging.Formatter(fmt,style='%')
    
    my_logger.setLevel(logging.DEBUG)
    fmt = '[%(levelname)s] %(asctime)s - %(message)s'
    log_formatter_b =logging.Formatter(fmt,style='%')
    
    stream_handler=logging.StreamHandler()
    stream_handler.setFormatter(log_formatter_a)
    stream_handler.setFormatter(log_formatter_b)
    #Here U set the minimum level to be streamed to terminal
    stream_handler.setLevel(logging.DEBUG)

    my_logger.addHandler(stream_handler)

    return my_logger

# logger.disabled = True
