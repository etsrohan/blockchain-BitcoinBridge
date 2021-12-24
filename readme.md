# How to run the system

### Supply Chain - Ganache

#### Step 1:
![Step1] (Images/Step 1.png?raw=true)

Open Ganache using the downloaded AppImage downloaded from the ganache website. Click on quickstart when prompted.

#### Step 2:
![Step2] (Images/Step 2.png)

Navigate to the downloaded code folder and open the `base` folder. Open a terminal and type in `python3 SRC/deploy_contract.py` and press enter.

#### Step 3:
![Step3] (Images/Step 3.png)

Open another terminal in the same `base` folder and type in `python3 SRC/event_listener.py` and press enter. Position these 2 terminals as you see fit.

#### Step 4:
![Step4] (Images/Step 4.png)

In the terminal where you deployed the system type in `python3 SRC/create_delivery_sc.py` to create a new order for the delivery of raw materials.

#### Step 5:
![Step5] (Images/Step 5.png)

Next execute `python3 SRC/order_delivered_sc.py` and enter the Delivery ID when prompted.

#### Step 6:
![Step6] (Images/Step 6.png)

To start manufacturing execute `python3 SRC/start_batch_sc.py` select the type of material to use and the apparel to make.

#### Step 7:
![Step7] (Images/Step 7.png)

To complete a batch execute `python3 SRC/complete_batch_sc.py` when detemining the output of the manufacturing process do keep it under 200 as it will then cause problems with gas price.

#### Step 8:
![Step8] (Images/Step 8.png)

In order to proceed to sales we need to ship the batch of clothes. So type in `python3 SRC/ship_batch_sc.py` and enter the batch number given by the event listener.

#### Step 9:
![Step9] (Images/Step 9.png)

To sell a particular item created by the processing batch execute `python3 SRC/sell_item_sc.py` select one of the item numbers created in the previous step and add all the necessary details.

### Step 10:
![Step10] (Images/Step 10.png)

To return a sold item we need to execute `python3 SRC/return_item_sc.py` and enter the item number to be returned. Note: you cannot return an item that does not exist or that has not been sold.
