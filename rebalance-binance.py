import ccxt
from songline import Sendline

while True:
  apiKey = "QPreLBCnzw9cwwFGL9OBbvZ9N6kWCa7mERnDbGkpLsrKg2vq7HdZgt4jMsw0wtmq" #@param {type:"string"}
  secret = "toNyqtuIdoErW0KtNQk6Mz7oyfYtsI7hFGlfVoaGIo4P22OEWkllqbXOcpCkRDsb" #@param {type:"string"}
  password = ""                   #@param {type:"string"}
  Account_name  = "BINANCE"           #@param {type:"string"}

  pair_trade = 'BTC/USDT'          #@param {type:"string"}
  Asset_RB   = 'BTC'              #@param {type:"string"}
  Asset_Base = 'USDT'             #@param {type:"string"}

  Rebalance_percent = 5.5           #@param 

  line_token = 'ARnYmPCo1HMmnXJxFBHRtUALbWoEBnpSDZ7bYHpX562'  #@param {type:"string"}
  messenger = Sendline(line_token)

####################################################
  exchange = ccxt.binance  ({
    'apiKey' : apiKey ,'secret' : secret ,'password' : password ,'enableRateLimit': True
  })
  # Sub Account Check
  if Account_name == "" :
    print("\n""Account Name - This is Main Account",': Broker - ',exchange)     
  else:
    print( "\n"'Account Name - ',Account_name,': Broker - ',exchange)
    exchange.headers = {
      'ftx-SUBACCOUNT': Account_name,
    }
  print("#########################################")
  get_price     = exchange.fetch_ticker(pair_trade) 
  Average_price = (get_price ['bid'] + get_price ['ask'])/2
  Get_balance = exchange.fetch_balance()          #โค้ดดึงยอด Asset ทั้งบัญชี
  Asset_01 = Get_balance [Asset_RB] ['total']     #ดึงยอดตัวที่ Rebalance
  Asset_02 = Get_balance [Asset_Base] ['total']   #ดึงยอดตัว Base
  Sum_Asset = Asset_01*Average_price + Asset_02 

  print(Asset_RB, " Price = ", round(Average_price,2)) #ราคาของ Asset 1 ณ ตอนรันโค้ด
  print(Asset_RB, " Value = " , Asset_01*Average_price, "(",round(((Asset_01*Average_price)/Sum_Asset)*100,2),"%)" )   #มูลค่าของ Asset 1
  print(Asset_Base, " Value = " , Asset_02, "(",round(((Asset_02)/Sum_Asset)*100,2),"%)" )                  #มูลค่าของ Asset 2
  print("All Asset = ", Sum_Asset, "USD")                     #รวมมูลค่าของ Asset ทั้งหมดในบัญชี
  print("#########################################")
  
  
  Rebalance_mark = Sum_Asset/2
  diff_asset = (Asset_01*Average_price)-Rebalance_mark
  print("Diff Asset :", round(diff_asset,2), "USD")
  print("Diff Asset % :", round((diff_asset/Rebalance_mark)*100,2), "%" )
  # มูลค่า ของ Asset
  Asset_01_Value = Asset_01 * Average_price
  #print("Asset_01_Value = " ,Asset_01_Value)
  print("#########################################")

  if   Asset_01_Value > (Rebalance_mark + (Rebalance_mark*Rebalance_percent/100) ) :
    print("Asset_01_Value ",Asset_01_Value ,">", (Rebalance_mark + (Rebalance_mark*Rebalance_percent/100) ))
    print("SELL")
    diff_sell  = Asset_01_Value - Rebalance_mark
    diff_sell_str = str(diff_sell)
    print(diff_sell)
    messenger.sendtext("Rebalance Status : Sell " + diff_sell_str + "USD")
    exchange.create_order(pair_trade ,'market','sell',(diff_sell/Average_price))

  elif Asset_01_Value < (Rebalance_mark - (Rebalance_mark*Rebalance_percent/100) ) :
    print("Asset_01_Value ",Asset_01_Value ,"<", (Rebalance_mark - (Rebalance_mark*Rebalance_percent/100) ))
    print("Buy")
    diff_buy  = Rebalance_mark - Asset_01_Value
    diff_buy_str = str(diff_buy)
    print(diff_buy)
    messenger.sendtext("Rebalance Status : Buy " + diff_buy_str + "USD")
    exchange.create_order(pair_trade ,'market','buy',(diff_buy/Average_price))
    
  else :
    print("None Trade")
    #messenger.sendtext("None Trade")

  import time
  sleep = 300 #ระยะเวลาดีเลย์ของสคริปก่อนจะรันใหม่ (หน่วยเป็นวินาที)
  print("Sleep",sleep,"sec.")
  time.sleep(sleep) # Delay for 1 minute (60 seconds).  
