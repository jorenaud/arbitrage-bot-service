from enum import Enum, auto

# 1: logout, 2: login, -1: close, 0: no email, 3: trading
class trader_status(Enum):
    Closed = -1
    No_email_verify = 0
    Logout = 1
    Login = 2
    Trading = 3



class PosAccMethod(Enum):
    Default = 0
    Netting = auto()
    Hedging = auto()

class MarginMode(Enum):
    MarginForex = 0
    MarginFutures = auto()
    vMarginCFD = auto()
    MarginCFDIndex = auto()



class TradeMode(Enum):
    Disabled = 0
    LongOnly = auto()
    ShortOnly = auto()
    CloseOnly = auto()
    FullAccess = auto()

class ExecutionType(Enum):
    Request = 0
    Instant = auto()
    Market = auto()
    Exchange = auto()

class SwapType(Enum):
    SwapNone = 0
    InPoints = auto()
    SymInfo_s408 = auto()
    MarginCurrency = auto()
    Currency = auto()
    PercCurPrice = auto()
    PercOpenPrice = auto()
    PointClosePrice = auto()
    PointBidPrice = auto()

class V3DaysSwap(Enum):
    Sunday = 0
    Monday = auto()
    Tuesday = auto()
    Wednesday = auto()
    Thursday = auto()
    Friday = auto()
    Saturday = auto()


class Direction(Enum):
    In = 0
    Out = 1
    InOut = 2
    OutBy = 3

class PlacedType(Enum):
    Manually = 0
    ByExpert = auto()
    ByDealer = auto()
    OnSL = auto()
    OnTP = auto()
    OnStopOut = auto()
    OnRollover = auto()
    Mobile = 16
    Web = auto()

class ExpirationDate(Enum):
    GTC = 0
    Today = 1
    Specified = 2
    SpecifiedDay = 3

class FillPolicy(Enum):
    FillOrKill = 0
    ImmediateOrCancel = 1
    FlashFill = 2

class OrderType(Enum):
    Buy = 0
    Sell = auto()
    BuyLimit = auto()
    SellLimit = auto()
    BuyStop = auto()
    SellStop = auto()
    BuyStopLimit = auto()
    SellStopLimit = auto()
    All = auto()

class TradeType(Enum):
    TradePrice = 0
    RequestExecution = auto()
    InstantExecution = auto()
    MarketExecution = auto()
    ExchangeExecution = auto()
    SetOrder = auto()
    ModifyDeal = auto()
    ModifyOrder = auto()
    CancelOrder = auto()
    Transfer = auto()
    ClosePosition = auto()
    ActivateOrder = 100
    ActivateStopLoss = auto()
    ActivateTakeProfit = auto()
    ActivateStopLimitOrder = auto()
    ActivateStopOutOrder = auto()
    ActivateStopOutPosition = auto()
    ExpireOrder = auto()
    ForSetOrder = 200
    ForOrderPrice = auto()
    ForModifyDeal = auto()
    ForModifyOrder = auto()
    ForCancelOrder = auto()
    ForActivateOrder = auto()
    ForBalance = auto()
    ForActivateStopLimitOrder = auto()
    ForClosePosition = auto()

class OrderState(Enum):
    Started = 0
    Placed = auto()
    Canceled = auto()
    Partial = auto()
    Filled = auto()
    Rejected = auto()
    Expired = auto()
    RequestAdding = auto()
    RequestModifying = auto()
    RequestCancelling = auto()


class SymbolGroup(Enum):
    MajorForex = 1
    SpotGold = 2
    ShShares = 3

class CalculationMode(Enum):
    vForex = 0
    vFutures = auto()
    vCFD = auto()
    vCFDIndex = auto()
    vCFDLeverage = auto()
    vCalcMode5 = auto()
    vExchangeStocks = 32
    vExchangeFutures = auto()
    vFORTSFutures = auto()
    vExchangeOption = auto()
    vExchangeMarginOption = auto()
    vExchangeBounds = auto()
    vCollateral = 64

class GTCMode(Enum):
    Cancelled = 0
    TodayIncludeSL_TP = auto()
    TodayExcludeSL_TP = auto()
