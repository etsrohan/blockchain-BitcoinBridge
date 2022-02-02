// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract ClothingSupplyChain{
    // ENUMS
    enum ApparelType {Unknown, Shirt, TShirt, Pants}
    enum FabricType {Unknown, Cotton, Polyester}

    // STRUCTS
    struct clothing{
        string name;
        string manufacturer;
        string department;
        uint256 weight; // in grams
        uint256 price; // in US cents
        uint256 num_items;
    }

    // EVENTS
    event added_products(ApparelType indexed apparel, FabricType indexed fabric, uint256 num_added);
    event items_bought(uint256[6] num_buy);
    event items_defective(uint256[6] num_defective);

    // MODIFIERS
    modifier admin_only(){
        require(msg.sender == admin);
        _;
    }
    // VARIABLES
    address admin;

    mapping (ApparelType => mapping (FabricType => clothing)) clothes;

    // FUNCTIONS
    constructor () {
        admin = msg.sender;
        create_clothes(ApparelType.Shirt, FabricType.Cotton, 150, 1500, "Cotton Shirt");
        create_clothes(ApparelType.Shirt, FabricType.Polyester, 100, 1600, "Polyester Shirt");
        create_clothes(ApparelType.TShirt, FabricType.Cotton, 80, 1000, "Cotton T-Shirt");
        create_clothes(ApparelType.TShirt, FabricType.Polyester, 50, 1200, "Polyester T-Shirt");
        create_clothes(ApparelType.Pants, FabricType.Cotton, 200, 3000, "Cotton Pants");
        create_clothes(ApparelType.Pants, FabricType.Polyester, 180, 3500, "Polyester Pants");
    }

    // A Function to create the 6 clothing groups
    // i.e. Cotton Shirt/T-Shirt/Pants and Polyester Shirt/T-Shirt/Pants
    // along with their initial prices and weights
    // Cotton Shirt: 150g, $15.00; Cotton T-Shirt: 80g, $10.00; Cotton Pants: 200g, $30.00
    // Polyester Shirt: 100g, $16.00; Polyester T-Shirt: 50g, $12.00; Polyester Pants: 180g, $35.00
    function create_clothes(
        /**ARGUMENTS**/
        ApparelType apparel,
        FabricType fabric,
        uint256 weight,
        uint256 price,
        string memory name
    )
        internal
        returns (bool)
    {
        clothes[apparel][fabric].name = name;
        clothes[apparel][fabric].manufacturer = "Shereen Clothes Pvt. Ltd.";
        clothes[apparel][fabric].department = "mens";
        clothes[apparel][fabric].weight = weight;
        clothes[apparel][fabric].price = price;
        clothes[apparel][fabric].num_items = 100;

        return true;
    }

    // A function to change the weight or prices of a particular item
    // If weight or price is 0 then it is skipped
    function change_clothes(
        /**ARGUMENTS**/
        ApparelType apparel,
        FabricType fabric,
        uint256 price,
        uint256 weight
    )
        public
        admin_only()
        returns (bool)
    {
        require(apparel != ApparelType.Unknown, "Apparel Invalid");
        require(fabric != FabricType.Unknown, "Fabric Invalid");
        
        if (price != 0) clothes[apparel][fabric].price = price;
        if (weight != 0) clothes[apparel][fabric].weight = weight;

        return true;
    }

    // A function used to add more inventory to the existing supply in 
    // the warehouse
    function add_products(
        /**ARGUMENTS**/
        ApparelType apparel,
        FabricType fabric,
        uint256 num_added
    )
        public
        admin_only()
        returns (bool)
    {
        require(num_added > 0, "Must add num of items > 0");

        clothes[apparel][fabric].num_items += num_added;
        emit added_products(apparel, fabric, num_added);
        return true;
    }

    // A function to a certain number of products
    // To be used by buy_product or defective_product functions
    function remove_products(
        /**ARGUMENTS**/
        ApparelType apparel,
        FabricType fabric,
        uint256 num_remove
    )
        internal
        returns (bool)
    {
        require(num_remove > 0, "Must remove num of items > 0");
        require(num_remove < clothes[apparel][fabric].num_items, "Cannot remove more items than already existing!");

        clothes[apparel][fabric].num_items -= num_remove;
        return true;
    }

    // A function to buy certain products from the seller
    // and subsequently remove them from warehouse
    function buy_product(
        /**ARGUMENTS**/
        uint256[6] memory num_buy
    )
        public
        returns (bool)
    {
        ApparelType apparel;
        FabricType fabric;
        for (uint i = 0; i < 6; i++){
            // Check to see if we want to buy this item/
            if (num_buy[i] == 0) continue;

            // Get apparel
            if ((i / 2) == 0) apparel = ApparelType.Shirt;
            else if ((i / 2) == 1) apparel = ApparelType.TShirt;
            else apparel = ApparelType.Pants;

            // Get Fabric
            if ((i % 2) == 0) fabric = FabricType.Cotton;
            else fabric = FabricType.Polyester;

            // Remove items from stock
            remove_products(apparel, fabric, num_buy[i]);
        }

        emit items_bought(num_buy);
        return true;
    }

    // 
    function defective_products(
        /**ARGUMENTS**/
        uint256[6] memory num_defective
    )
        public
        admin_only()
        returns (bool)
    {
        ApparelType apparel;
        FabricType fabric;
        for (uint i = 0; i < 6; i++){
            // Check to see if we want to buy this item/
            if (num_defective[i] == 0) continue;

            // Get apparel
            if ((i / 2) == 0) apparel = ApparelType.Shirt;
            else if ((i / 2) == 1) apparel = ApparelType.TShirt;
            else apparel = ApparelType.Pants;

            // Get Fabric
            if ((i % 2) == 0) fabric = FabricType.Cotton;
            else fabric = FabricType.Polyester;

            // Remove items from stock
            remove_products(apparel, fabric, num_defective[i]);
        }

        emit items_defective(num_defective);
        return true;
    }

    // A function to get the product information
    function inquire_product(
        /**ARGUMENTS**/
        ApparelType apparel,
        FabricType fabric
    )
        public
        view
        returns (clothing memory)
    {
        return clothes[apparel][fabric];
    }
}