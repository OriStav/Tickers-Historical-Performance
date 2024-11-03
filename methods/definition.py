import inspect
import pandas as pd
import logging

class defs:
    def __init__(self,ui_choices: dict) -> None:
        if ui_choices:
            self.durations = ui_choices["durations"]
            self.symbols = ui_choices["symbols"]
            self.lst_wthrwl = ui_choices["lst_wthrwl"]
        else:
            self.durations=[3]#[3,5,10,15]#years
            self.symbols=["IGRO.AX","IBAL.AX" ,"IXI.AX" ,"VGS.AX",
                    "^GSPC","GBTC","TA35.TA"]
            self.lst_wthrwl=0#Years Ago

        self.report=False
        self.logger = set_logger()

def from_definition():
    bol_DataSource = tickers["DataSource"].apply(lambda x: x=="yfinance").to_list()
    bol=pd.DataFrame(bol_DataSource,tickers["Analyze"]).reset_index()
    bol=bol.all(axis='columns').to_list()
    return tickers.loc[bol,"Symbol"].drop_duplicates().to_list()

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

#%%
import pandas as pd
tickers = pd.DataFrame({"Symbol": [
        "TCEHY", "BABA", "KWEB", "GOOGL", "AAPL", "AMZN", "NFLX", "BRK-B", "GSPC", 
        "META", "WYNN", "GIS", "NDX", "RUT", "DJI", "FTSE", "GDAXI", "TA35.TA", 
        "TA90.TA", "N225", "HSI", "NSEI", "STOXX", "SOXX", "ACWI", "IEMG", "URTH", 
        "SWRD.L", "SSO", "UPRO", "STRS.TA", "SPEN.TA", "ELTR.TA", "VTNA.TA", "NICE.TA",
        "ICL.TA", "PHOE.TA", "FIBI.TA", "ORA.TA", "AZRG.TA", "GLTC.TA", "GLRS.TA", 
        "IMCO.TA", "ISCD.TA", "ISCN.TA", "MNRT.TA", "MNRA.TA", "ESTATE15.TA", 
        "MVNE.TA", "MLSR.TA", "RIT1.TA", "AMOT.TA", "ASHO.TA", "IBM", "SAP", "SIEGY", 
        "MSFT", "GE", "INTC", "BOSCHLTD.BO", "BOSCHLTD.NS", "SAP", "MSFT", "AI", 
        "XAO.AX", "IBIT", "SOS", "RIOT", "BITF", "MARA", "HUT", "CMS", "FSLR", "GOOGL", 
        "AMZN", "VRT", "NOK", "CARR", "CC", "TT", "JCI", "DKILY", "005930.KS", "DNZOY", 
        "VLEEY", "018880.KS", "GOOGL", "INTC", "GIS", "GS", "AAPL", "NKE", "HITI.V", 
        "TXN", "TSM", "SWK", "UFPI", "CENT", "HD", "NICE.TA", "MLSR.TA", "AZRG.TA", 
        "SPEN.TA", "VTNA.TA", "RIT1.TA", "META", "TSLA", "BABA", "TCEHY", "KWEB", 
        "BTC-USD", "005930.KS", "EADSY", "GOOGL", "NKE", "BOSCHLTD.BO", "CRM", "ORCL", 
        "ADBE", "HD", "DKILY", "018880.KS", "BRK-B", "AAPL", "AMZN", "NFLX", "EVTL", 
        "VTNA.TA", "LILM", "QS", "TSLA", "TM", "TOYOF", "EADSY", "FCEL", "BLDP", "PLUG", 
        "CVX", "ILS=X", "BTC-USD", "DOGE-USD", "CRM", "ZEN", "HUBS", "ORCL", "ADBE", 
        "GC=F", "IGRO.AX", "IBAL.AX", "IXI.AX", "VAS.AX", "ASX.AX", "IRM", "EQIX", 
        "DLR", "SRVR", "VPN", "VPU", "OPC.HM", "GSY", "PULS", "SLQD", "IGSB", "IGRO.AX", 
        "IBAL.AX", "IXI.AX", "VAS.AX", "ASX.AX", "URTH", "XAO.AX", "RUT", "GC=F", "NSEI", 
        "AFHL.TA", "SKBNF.TA", "INTC", "WYNN", "TSLA", "GIS", "ORCL", "COST", "OPC.HM", 
        "VUG", "ADM", "SARK", "AFHL.TA", "SKBNF.TA", "VUG", "VOOG", "CPI", "COST", 
        "ADM", "SARK", "VGS.AX", "VGS.AX", "SWRD.L", "URTH", "RUT", "NSEI", "AFHL.TA", 
        "BTC-USD", "DOGE-USD", "ASX.AX", "IXI.AX", "IGRO.AX", "VGS.AX", "GOOGL", 
        "AMZN", "EQIX", "INTC", "TSLA", "GIS", "ADM", "RIOT"
    ],
    "Category": [
        "US Inverse", "US Inverse", "US Inverse", "TopUS", "TopUS", "TopUS", "TopUS", 
        "TopUS", "TopUS", "TopUS", "TopUS", "TopUS", "TopIndices", "TopIndices", 
        "TopIndices", "TopIndices", "TopIndices", "TopIndices", "TopIndices", 
        "TopIndices", "TopIndices", "TopIndices", "TopIndices", "TopIndices", 
        "TopIndices", "TopIndices", "TopIndices", "TopIndices", "TopIndices", 
        "TopIndices", "TA", "TA", "TA", "TA", "TA", "TA", "TA", "TA", "TA", "TA", 
        "TA", "TA", "TA", "TA", "TA", "TA", "TA", "TA", "TA", "TA", "TA", 
        "Predictive", "Predictive", "Predictive", "Predictive", "Predictive", 
        "Predictive", "Predictive", "Predictive", "Predictive", "Predictive", 
        "Predictive", "Aussie", "Crypto", "Crypto Miners", "Crypto Miners", 
        "Crypto Miners", "Crypto Miners", "Crypto Miners", "Data Centers", 
        "Data Centers", "Data Centers", "Data Centers", "Data Centers", "Loser", 
        "HVACR", "HVACR", "HVACR", "HVACR", "HVACR", "HVACR", "HVACR", 
        "Automotive_HVAC", "Automotive_HVAC", "Automotive_HVAC", "Hippie", 
        "Hippie", "Hippie", "Hippie", "Hippie", "Hippie", "Hippie", "Hardware", 
        "Hardware", "Hardware", "Hardware", "Hardware", "Hardware", "FocusTA", 
        "FocusTA", "FocusTA", "FocusTA", "FocusTA", "FocusTA", "Focus5", 
        "Focus5", "Focus4", "Focus4", "Focus4", "Focus4", "Focus3", "Focus3", 
        "Focus3", "Focus3", "Focus3", "Focus2", "Focus2", "Focus2", "Focus2", 
        "Focus2", "Focus1", "Focus1", "Focus1", "Focus1", "Focus1", "Focus1", 
        "EVTOL", "EVTOL", "EVTOL", "Energy", "Energy", "Energy", "Energy", 
        "Energy", "Energy", "Energy", "Energy", "Energy", "Currencies", 
        "Crypto", "Crypto", "CRM", "CRM", "CRM", "CRM", "CRM", "Commodities", 
        "Aussie", "Aussie", "Aussie", "Aussie", "Aussie", "Data Centers", 
        "Data Centers", "Data Centers", "Data Centers", "Data Centers", "Energy", 
        "MoneyMarket", "MoneyMarket", "MoneyMarket", "MoneyMarket", "Nov24AUD", 
        "Nov24AUD", "Nov24AUD", "Nov24AUD", "Nov24AUD", "Nov24AUD", "Nov24AUD", 
        "Nov24ILS", "Nov24ILS", "Nov24ILS", "Nov24USD", "Nov24USD", "Nov24USD", 
        "Nov24USD", "Nov24USD", "Nov24USD", "Nov24USD", "Nov24USD", "Nov24USD", 
        "Nov24USD", "Nov24USD", "Nov24USD", "TopIndices", "TopIndices", 
        "TopIndices", "TopUS", "TopUS", "US Inverse", "Aussie", "World", 
        "World", "World", "World", "Nov24", "Nov24", "Nov24", "Nov24", 
        "Nov24", "Nov24", "Nov24", "Nov24", "Nov24", "Nov24", "Nov24", 
        "Nov24", "Nov24", "Nov24", "Nov24", "Nov24", "Nov24", "Nov24", "Nov24"
    ]
})

