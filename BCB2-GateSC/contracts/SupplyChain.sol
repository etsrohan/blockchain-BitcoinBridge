// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract GateSupplyChain{
    // ENUMS
    enum GateType {Unknown, Nand, Nor}
    enum NumPins {Unknown, Six, Eight, Twelve, Fourteen}

    // STRUCTS
    struct chip{
        string name;
        string manufacturer;
        string department;
        uint256 price; // in US cents
        uint256 input_voltage; // in mV
        uint256 num_items;
        uint8 num_gates;
    }

    // EVENTS
    event added_products(GateType indexed gate, NumPins indexed pins, uint256 num_added);
    event items_bought(uint256[8] num_buy);
    event items_defective(uint256[8] num_defective);

    // MODIFIERS
    modifier admin_only(){
        require(msg.sender == admin);
        _;
    }
    // VARIABLES
    address admin;

    mapping (GateType => mapping (NumPins => chip)) chips;

    // FUNCTIONS
    constructor () {
        admin = msg.sender;
        create_chips(GateType.Nand, NumPins.Six, 30, 5000, "NAND-6", 1);
        create_chips(GateType.Nor, NumPins.Six, 27, 5000, "NOR-6", 1);
        create_chips(GateType.Nand, NumPins.Eight, 40, 3300, "NAND-8", 2);
        create_chips(GateType.Nor, NumPins.Eight, 35, 3300, "NOR-8", 2);
        create_chips(GateType.Nand, NumPins.Twelve, 50, 5000, "NAND-12", 3);
        create_chips(GateType.Nor, NumPins.Twelve, 45, 5000, "NOR-12", 3);
        create_chips(GateType.Nand, NumPins.Fourteen, 60, 5000, "NAND-14", 4);
        create_chips(GateType.Nor, NumPins.Fourteen, 55, 5000, "NOR-14", 4);
    }

    // A Function to create the 8 chip groups
    // i.e. NAND Six/Eight/Twelve/Fourteen pins and NOR Six/Eight/Twelve/Fourteen pins
    // along with their initial prices and operating voltages
    // NAND-6: $0.30, 5V; NAND-8: $0.40, 3.3V; NAND-12: $0.50, 5V; NAND-14: $0.60, 5V
    // NOR-6: $0.27, 5V; NOR-8: $0.35, 3.3V; NOR-12: $0.45, 5V; NOR-14: $0.55, 5V
    function create_chips(
        /**ARGUMENTS**/
        GateType gate,
        NumPins pins,
        uint256 price,
        uint256 voltage,
        string memory name,
        uint8 num_gates
    )
        internal
        returns (bool)
    {
        chips[gate][pins].name = name;
        chips[gate][pins].manufacturer = "XYZ Electronics Inc.";
        chips[gate][pins].department = "electrical";
        chips[gate][pins].price = price;
        chips[gate][pins].input_voltage = voltage;
        chips[gate][pins].num_items = 1000;
        chips[gate][pins].num_gates = num_gates;

        return true;
    }

    // A function to change the price or operating voltage of a particular item
    // If price or operating voltage is 0 then it is skipped
    function change_properties(
        /**ARGUMENTS**/
        GateType gate,
        NumPins pins,
        uint256 price,
        uint256 voltage
    )
        public
        admin_only()
        returns (bool)
    {
        require(gate != GateType.Unknown, "Gate Invalid");
        require(pins != NumPins.Unknown, "Number of Pins Invalid");
        
        if (price != 0) chips[gate][pins].price = price;
        if (voltage != 0) chips[gate][pins].input_voltage = voltage;

        return true;
    }

    // A function used to add more inventory to the existing supply in 
    // the warehouse
    function add_products(
        /**ARGUMENTS**/
        GateType gate,
        NumPins pins,
        uint256 num_added
    )
        public
        admin_only()
        returns (bool)
    {
        require(num_added > 0, "Must add num of items > 0");

        chips[gate][pins].num_items += num_added;
        emit added_products(gate, pins, num_added);
        return true;
    }

    // A function to a certain number of products
    // To be used by buy_product or defective_product functions
    function remove_products(
        /**ARGUMENTS**/
        GateType gate,
        NumPins pins,
        uint256 num_remove
    )
        internal
        returns (bool)
    {
        require(num_remove > 0, "Must remove num of items > 0");
        require(num_remove <= chips[gate][pins].num_items, "Cannot remove more items than already existing!");

        chips[gate][pins].num_items -= num_remove;
        return true;
    }

    // A function to buy certain products from the seller
    // and subsequently remove them from warehouse
    function buy_product(
        /**ARGUMENTS**/
        uint256[8] memory num_buy
    )
        public
        returns (bool)
    {
        GateType gate;
        NumPins pins;
        for (uint i = 0; i < 8; i++){
            // Check to see if we want to buy this item/
            if (num_buy[i] == 0) continue;

            // Get Number of Pins
            if ((i / 2) == 0) pins = NumPins.Six;
            else if ((i / 2) == 1) pins = NumPins.Eight;
            else if ((i / 2) == 2) pins = NumPins.Twelve;
            else pins = NumPins.Fourteen;

            // Get Gate Type
            if ((i % 2) == 0) gate = GateType.Nand;
            else gate = GateType.Nor;

            // Remove items from stock
            remove_products(gate, pins, num_buy[i]);
        }

        emit items_bought(num_buy);
        return true;
    }

    // A method used by the admin to return defective products
    function defective_products(
        /**ARGUMENTS**/
        uint256[8] memory num_defective
    )
        public
        admin_only()
        returns (bool)
    {
        GateType gate;
        NumPins pins;
        for (uint i = 0; i < 8; i++){
            // Check to see if we want to buy this item
            if (num_defective[i] == 0) continue;

            // Get Number of Pins
            if ((i / 2) == 0) pins = NumPins.Six;
            else if ((i / 2) == 1) pins = NumPins.Eight;
            else if ((i / 2) == 2) pins = NumPins.Twelve;
            else pins = NumPins.Fourteen;

            // Get Gate Type
            if ((i % 2) == 0) gate = GateType.Nand;
            else gate = GateType.Nor;

            // Remove items from stock
            remove_products(gate, pins, num_defective[i]);
        }

        emit items_defective(num_defective);
        return true;
    }

    // A function to get the product information
    function inquire_product(
        /**ARGUMENTS**/
        GateType gate,
        NumPins pins
    )
        public
        view
        returns (chip memory)
    {
        return chips[gate][pins];
    }
}