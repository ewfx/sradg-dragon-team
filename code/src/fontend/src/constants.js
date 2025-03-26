export const ihub={
    "key_columns": ["Company","Account","AU","Currency"],
    "criteria_columns": ["GL Balance","IHub Balance"],
    "derived_columns": ["Balance Difference"],
    "historic_columns": ["Account","Secondary Account","Primary Account"],
    "date_columns": ["As of Date"]
}

export const catalyst={
    "key_columns": ["TRADEID"],
    "criteria_columns": ["INVENTORY","CUSIP","TRADE_DATE","SETTLE_DATE","BUY_SELL","PRICE"],
    "historic_columns": ["INVENTORY","CUSIP"],
    "date_columns": ["RECONDATE"]
}