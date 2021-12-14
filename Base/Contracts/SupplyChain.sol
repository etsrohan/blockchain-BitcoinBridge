// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

contract ClothingSupplyChain{
    // ENUMS
    enum MaterialType {Unknown, Cotton, Ethylene}
    enum MaterialState {NotCreated, Enroute, Delivered, Failed}
    enum BatchType {Unknown, Cotton, Polyester}
    enum BatchState {NotCreated, Created, Shipped}
    enum ItemType {Unknown, TShirt, Shirt, Pants}
    enum SaleState {NotSold, Sold, Returned}

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
        BatchState state;
        uint256 manufacture_date;
        uint256 machine_id;
        uint256 num_clothes;
        uint256 price_per;          // price in cents per clothing made
        uint256 cost_per;           // cost in cents per clothing made
    }

    // Struct to represent an individual item
    struct Item {
        SaleState state;
        ItemType item_type;
        uint256 receipt_number;
        uint256 retail_price;
        uint256 date_of_sale;
        MaterialDelivery material;
        ManufactureBatch manufacturing;
    }

    // EVENTS
    event NewDeliveryCreated(uint256 indexed delivery_id, address employee_address, string supplier);
    event DeliveryCreationFailed(string supplier, uint8 material, uint256 weight, uint256 cost, string message);
    event DeliveryReceived (uint256 indexed delivery_id);
    event DeliveryCanceled (uint256 indexed delivery_id);
    event NewItemCreated(uint256 indexed item_id, uint8 item_type);

    // MODIFIERS
    modifier delivery_order_created (uint256 delivery_id){
        require (deliveries[delivery_id].state == MaterialState.Enroute);
        _;
    }

    // VARIABLES
    address admin;
    uint256 [2] private material_weights;
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

    // A function to create a delivery order for new materials
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

        emit NewDeliveryCreated(delivery_id, msg.sender, supplier_name);
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
        emit DeliveryCanceled(delivery_id);
        return true;
    }

    // A function to start processing a new batch of clothes being proccessed
    function start_manufacturing(
        /**Manufacturing Details**/

    )
        public
        returns (bool)
    {
        
    }
}