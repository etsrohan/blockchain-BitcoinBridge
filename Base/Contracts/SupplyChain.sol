// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

contract ClothingSupplyChain{
    // ENUMS
    enum MaterialType {Unknown, Cotton, Ethylene}
    enum MaterialState {NotCreated, Enroute, Delivered, Failed}
    enum BatchType {Unknown, Cotton, Polyester}
    enum BatchState {NotCreated, Processing, Complete, Shipped}
    enum ItemType {Unknown, TShirt, Shirt, Pants}
    enum ItemState {NotCreated, Created, Sold, Returned}

    // STRUCTS
    // Struct to represent a delivery of raw materials
    // from the supplier
    struct MaterialDelivery {
        MaterialType mat_type;
        MaterialState state;
        string supplier_name;
        uint256 date;
        uint256 weight;             // weight in grams
        uint256 cost;               // cost per kg in cents
    }

    // Struct to represent the final product of a batch
    // of manufactured clothes.
    struct ManufactureBatch {
        BatchType fabric_type;
        ItemType item_type;
        BatchState state;
        uint256 manufacture_date;
        uint256 machine_id;
        uint256 num_clothes;
        uint256 price_per;          // price in cents per clothing made
        uint256 cost_per;           // cost in cents per clothing made
    }

    // Struct to represent an individual item
    struct Item {
        ItemState state;
        uint256 batch_no;
        uint256 receipt_number;
        uint256 retail_price;       // price in cents for item
        uint256 date_of_sale;
    }

    // EVENTS
    event NewDeliveryCreated (uint256 indexed delivery_id, address employee_address, string supplier, MaterialType material);
    event DeliveryCreationFailed (string supplier, uint8 material, uint256 weight, uint256 cost, string message);
    event NewBatchCreated (uint256 indexed batch_id, address employee_address, BatchType fabric, ItemType apparel);
    event BatchCreationFailed (uint8 fabric, uint256 machine_id, string message);
    event BatchCompletionFailed (uint256 indexed batch_id, string message);
    event BatchCompleted (uint256 indexed batch_id, uint256 num_items);
    event DeliveryReceived (uint256 indexed delivery_id);
    event DeliveryCancelled( uint256 indexed delivery_id);
    event NewItemsCreated (uint256 indexed item_start_id, uint256 indexed item_end_id, BatchType fabric, ItemType item_type);
    event ItemSold (uint256 indexed item_id, uint256 indexed receipt_num, uint256 date);
    event ItemReturned (uint256 indexed item_id, uint256 indexed receipt_num, uint256 date, uint256 price);

    // MODIFIERS
    modifier delivery_order_created (uint256 delivery_id){
        require (deliveries[delivery_id].state == MaterialState.Enroute);
        _;
    }

    modifier batch_processing (uint256 batch_id){
        require (batches[batch_id].state == BatchState.Processing);
        _;
    }

    modifier batch_complete (uint256 batch_id){
        require (batches[batch_id].state == BatchState.Complete);
        _;
    }

    modifier item_created (uint256 item_id){
        require (items[item_id].state == ItemState.Created);
        _;
    }

    modifier item_shipped (uint256 item_id){
        require (batches[items[item_id].batch_no].state == BatchState.Shipped);
        _;
    }

    modifier item_sold (uint256 item_id){
        require (items[item_id].state == ItemState.Sold);
        _;
    }

    // VARIABLES
    address admin;
    uint256 [2] private material_weights;   // amount of material available; 0 -> Cotton, 1 -> Ethylene
    uint256 [6] private num_apparel;        // Stock of Apparel: 0 -> cotton tshirt, 1 -> polyester tshirt, 2 -> cotton shirt, 3 -> polyester shirt, 4 -> cotton pants, 5 -> polyester pants
    uint256 private num_deliveries;
    uint256 private num_batches;
    uint256 private num_items;

    mapping (uint256 => MaterialDelivery) deliveries;
    mapping (uint256 => ManufactureBatch) batches;
    mapping (uint256 => Item) items;
    
    // FUNCTIONS
    constructor ()
    {
        admin = msg.sender;
    }

    // --------------------------Supplier--------------------------
    // A function to create a delivery order for new materials
    // Material Type: 0 -> cotton, 1 -> Ethylene
    // weight = weight in grams
    // cost = cost in cents
    function create_delivery_order(
        /**Material Details**/
        uint8 material_type,
        string memory supplier_name,
        uint256 weight,
        uint256 cost
    )
        public
        returns (bool)
    {
        // Require non-zero weight and cost of material
        require (weight > 0, "Weight of delivery has to be more than 0");
        require (cost > 0, "Cost of delivery has to be more than 0");
        uint256 delivery_id = num_deliveries++;

        // Put correct material type in order
        // 0 -> Cotton, 1 -> Ethylene
        if (material_type == 0) deliveries[delivery_id].mat_type = MaterialType.Cotton;
        else if (material_type == 1) deliveries[delivery_id].mat_type = MaterialType.Ethylene;
        else {
            num_deliveries--;
            emit DeliveryCreationFailed(
                supplier_name, 
                material_type,
                weight,
                cost,
                "Incorrect Material Type"
            );
            return false;
        }

        // Filling in the other values for order
        deliveries[delivery_id].state = MaterialState.Enroute;
        deliveries[delivery_id].supplier_name = supplier_name;
        deliveries[delivery_id].weight = weight;
        deliveries[delivery_id].cost = cost;

        emit NewDeliveryCreated(delivery_id, msg.sender, supplier_name, deliveries[delivery_id].mat_type);
        return true;
    }

    // A function to successfull compete an order delivery
    function order_delivered(
        /**Order ID**/
        uint256 delivery_id
    )
        public
        delivery_order_created(delivery_id)
        returns (bool)
    {
        deliveries[delivery_id].date = block.timestamp;
        deliveries[delivery_id].state = MaterialState.Delivered;
        material_weights[0] += deliveries[delivery_id].weight;
        emit DeliveryReceived(delivery_id);
        return true;
    }

    // A function to cancel an enroute order
    function cancel_order(
        /**Order ID**/
        uint256 delivery_id
    )
        public
        delivery_order_created(delivery_id)
        returns (bool)
    {
        deliveries[delivery_id].state = MaterialState.Failed;
        emit DeliveryCancelled(delivery_id);
        return true;
    }

    
    // --------------------------Manufacture--------------------------
    // A function to start processing a new batch of clothes being proccessed
    // Fabric: 0 -> Cotton, 1 -> Polyester
    // Apparel: 0 -> tshirt, 1 -> shirt, 2 -> pants
    function start_batch(
        /**Batch Details**/
        uint8 fabric,
        uint8 apparel,
        uint256 machine_id
    )
        public
        returns (bool)
    {
        uint256 batch_id = num_batches++;

        // Put correct fabric type in order
        // 0 -> Cotton, 1 -> Ethylene
        if (fabric == 0) batches[batch_id].fabric_type = BatchType.Cotton;
        else if (fabric == 1) batches[batch_id].fabric_type = BatchType.Polyester;
        else {
            num_batches--;
            emit BatchCreationFailed(
                fabric,
                machine_id,
                "Incorrect Fabric Type"
            );
            return false;
        }

        // Put correct apparel type in order
        // 0 -> T-Shirt, 1 -> Shirt, 2 -> Pants
        if (apparel == 0) batches[batch_id].item_type = ItemType.TShirt;
        else if (apparel == 1) batches[batch_id].item_type = ItemType.Shirt;
        else if (apparel == 2) batches[batch_id].item_type = ItemType.Pants;
        else {
            num_batches--;
            emit BatchCreationFailed(
                fabric,
                machine_id,
                "Incorrect Apparel Type"
            );
            return false;
        }

        batches[batch_id].machine_id = machine_id;
        batches[batch_id].state = BatchState.Processing;
        emit NewBatchCreated(batch_id, msg.sender, batches[batch_id].fabric_type, batches[batch_id].item_type);
        return true;
    }

    // A function to end manufacture of an apparel
    // Assume 1 item requires 250g of material
    function complete_batch(
        /**Batch Details**/
        uint256 batch_id,
        uint256 batch_output,
        uint256 price,
        uint256 cost
    )
        public
        batch_processing(batch_id)
        returns (bool)
    {
        require (price > 0, "Price cannot be zero");
        require (cost > 0, "Cost cannot be zero");

        if (batches[batch_id].fabric_type == BatchType.Cotton){
            require (material_weights[0] >= batch_output * 250);
            material_weights[0] -= batch_output * 250;
        } else if (batches[batch_id].fabric_type == BatchType.Polyester){
            require (material_weights[1] >= batch_output * 250);
            material_weights[1] -= batch_output * 250;
        } else {
            emit BatchCompletionFailed(batch_id, "Batch not Initiated");
            return false;
        }
        
        batches[batch_id].state = BatchState.Complete;
        batches[batch_id].manufacture_date = block.timestamp;
        batches[batch_id].num_clothes = batch_output;
        batches[batch_id].price_per = price;
        batches[batch_id].cost_per = cost;

        // Create Items with the tagged details
        create_item(batch_id);

        emit BatchCompleted (batch_id, batches[batch_id].num_clothes);
        return true;
    }

    // Function to help add num of apparels in a batch to stock at store
    function add_apparel(
        /**Arguments**/
        uint256 batch_id
    )
        internal
        batch_complete(batch_id)
    {
        if ((batches[batch_id].fabric_type == BatchType.Cotton) &&
            (batches[batch_id].item_type == ItemType.TShirt)){
            num_apparel[0] += batches[batch_id].num_clothes;
        } else if ((batches[batch_id].fabric_type == BatchType.Polyester) &&
                   (batches[batch_id].item_type == ItemType.TShirt)){
            num_apparel[1] += batches[batch_id].num_clothes;
        } else if ((batches[batch_id].fabric_type == BatchType.Cotton) &&
                   (batches[batch_id].item_type == ItemType.Shirt)){
            num_apparel[2] += batches[batch_id].num_clothes;
        } else if ((batches[batch_id].fabric_type == BatchType.Polyester) &&
                   (batches[batch_id].item_type == ItemType.Shirt)){
            num_apparel[3] += batches[batch_id].num_clothes;
        } else if ((batches[batch_id].fabric_type == BatchType.Cotton) &&
                   (batches[batch_id].item_type == ItemType.Pants)){
            num_apparel[4] += batches[batch_id].num_clothes;
        } else if ((batches[batch_id].fabric_type == BatchType.Polyester) &&
                   (batches[batch_id].item_type == ItemType.Pants)){
            num_apparel[5] += batches[batch_id].num_clothes;
        }
    }

    // Function to create the number of items made in a batch
    function create_item(
        /**Batch ID**/
        uint256 batch_id
    )
        internal
        batch_complete(batch_id)
    {
        uint256 item_start = num_items;
        num_items += batches[batch_id].num_clothes;

        // Create new items and set state to 'Created'
        for (uint256 i = item_start; i < num_items; i++){
            items[i].state = ItemState.Created;
            items[i].batch_no = batch_id;
        }

        emit NewItemsCreated(
            item_start,
            num_items - 1,
            batches[batch_id].fabric_type,
            batches[batch_id].item_type
        );
    }

    // A function to ship the batch of items
    function ship_batch(
        /**Batch ID**/
        uint256 batch_id
    )
        public
        batch_complete(batch_id)
        returns (bool)
    {
        add_apparel(batch_id);
        batches[batch_id].state = BatchState.Shipped;

        return true;
    }

    // --------------------------Sale--------------------------
    // A function to sell an item from stock
    function sell_item(
        /**Sale Details**/
        uint256 item_id,
        uint256 receipt_number,
        uint256 price
    )
        public
        item_created(item_id)
        item_shipped(item_id)
        returns (bool)
    {
        items[item_id].state = ItemState.Sold;
        items[item_id].receipt_number = receipt_number;
        items[item_id].retail_price = price;
        items[item_id].date_of_sale = block.timestamp;

        // Subtract item from available stock
        subtract_stock(item_id);

        emit ItemSold (item_id, receipt_number, items[item_id].date_of_sale);

        return true;
    }

    // A helper function to subtract an item from the available stock
    // of ready to sell items.
    function subtract_stock(
        uint256 item_id
    )
        internal
    {
        uint256 batch_id = items[item_id].batch_no;
        if ((batches[batch_id].fabric_type == BatchType.Cotton) &&
            (batches[batch_id].item_type == ItemType.TShirt)){
            num_apparel[0] -= 1;
        } else if ((batches[batch_id].fabric_type == BatchType.Polyester) &&
                   (batches[batch_id].item_type == ItemType.TShirt)){
            num_apparel[1] -= 1;
        } else if ((batches[batch_id].fabric_type == BatchType.Cotton) &&
                   (batches[batch_id].item_type == ItemType.Shirt)){
            num_apparel[2] -= 1;
        } else if ((batches[batch_id].fabric_type == BatchType.Polyester) &&
                   (batches[batch_id].item_type == ItemType.Shirt)){
            num_apparel[3] -= 1;
        } else if ((batches[batch_id].fabric_type == BatchType.Cotton) &&
                   (batches[batch_id].item_type == ItemType.Pants)){
            num_apparel[4] -= 1;
        } else if ((batches[batch_id].fabric_type == BatchType.Polyester) &&
                   (batches[batch_id].item_type == ItemType.Pants)){
            num_apparel[5] -= 1;
        }
    }

    // A function to return the item that has already been sold
    function return_item(
        uint256 item_id
    )
        public
        item_sold(item_id)
        returns (bool)
    {
        items[item_id].state = ItemState.Returned;
        items[item_id].date_of_sale = block.timestamp;

        emit ItemReturned(
            item_id,
            items[item_id].receipt_number,
            items[item_id].date_of_sale,
            items[item_id].retail_price
        );

        return true;
    }

    function get_price(
        uint256 item_id
    )
        public
        view
        returns (uint256)
    {
        return items[item_id].retail_price;
    }
}