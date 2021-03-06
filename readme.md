# How to run the system

### Supply Chain - Ganache

#### Step 1:
![Step1](./Images/Step%201.png)

Open Ganache using the downloaded AppImage downloaded from the ganache website. Click on quickstart when prompted.

#### Step 2:
![Step2](./Images/Step%202.png)

Navigate to the downloaded code folder and open the `base` folder. Open a terminal and type in `python3 SRC/deploy_contract.py` and press enter.

#### Step 3:
![Step3](Images/Step%203.png)

Open another terminal in the same `base` folder and type in `python3 SRC/event_listener.py` and press enter. Position these 2 terminals as you see fit.

#### Step 4:
![Step4](Images/Step%204.png)

In the terminal where you deployed the system type in `python3 SRC/create_delivery_sc.py` to create a new order for the delivery of raw materials.

#### Step 5:
![Step5](Images/Step%205.png)

Next execute `python3 SRC/order_delivered_sc.py` and enter the Delivery ID when prompted.

#### Step 6:
![Step6](Images/Step%206.png)

To start manufacturing execute `python3 SRC/start_batch_sc.py` select the type of material to use and the apparel to make.

#### Step 7:
![Step7](Images/Step%207.png)

To complete a batch execute `python3 SRC/complete_batch_sc.py` when detemining the output of the manufacturing process do keep it under 200 as it will then cause problems with gas price.

#### Step 8:
![Step8](Images/Step%208.png)

In order to proceed to sales we need to ship the batch of clothes. So type in `python3 SRC/ship_batch_sc.py` and enter the batch number given by the event listener.

#### Step 9:
![Step9](Images/Step%209.png)

To sell a particular item created by the processing batch execute `python3 SRC/sell_item_sc.py` select one of the item numbers created in the previous step and add all the necessary details. Use the same receipt number to add item to the same transaction.

### Step 10:
![Step10](Images/Step%2010.png)

To return a sold item we need to execute `python3 SRC/return_item_sc.py` and enter the item number to be returned. Note: you cannot return an item that does not exist or that has not been sold.

### Step 11:

To proceed with the payment of the transaction execute `python3 SRC/pay_transaction.py`. This will conclude the receipt and send the appropriate amount of bitcoin from one address to another.
