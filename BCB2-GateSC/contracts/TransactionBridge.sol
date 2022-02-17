// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

contract TransactionBridge {
    // ENUMS
    enum TransactionState {NotCreated, Created, Completed, Failed, Refunded}

    // STRUCTS
    struct Transaction {
        TransactionState state;
        uint256[] items;
        uint256 total;             // Amount Due/Paid/Refunded in cents
        uint256[3] dates;          // Creation, Completion, Refund Dates in epoch time.
        bool seller_ok;
        bool buyer_ok;
    }

    // EVENTS
    event TransactionCreated (uint256 indexed receipt_number);
    event TransactionUpdated (uint256 indexed receipt_number, uint256 total);
    event TransactionRefunded (uint256 indexed receipt_number, uint256 total);
    event PaymentInitiated (uint256 indexed receipt_number, uint256 total);
    event SellerOk (uint256 indexed receipt_number, uint256 total);
    event BuyerOk (uint256 indexed receipt_number, uint256 total);

    // MODIFIERS
    modifier transaction_created(uint256 receipt_number){
        require(transactions[receipt_number].state == TransactionState.Created, "Transaction Not Created!");
        _;
    }

    modifier transaction_completed(uint256 receipt_number){
        require(transactions[receipt_number].state == TransactionState.Completed, "Transaction Not Completed!");
        _;
    }

    modifier transaction_payable(uint256 receipt_number){
        require(
            transactions[receipt_number].state == TransactionState.Created ||
            transactions[receipt_number].state == TransactionState.Failed,
            "Transaction already paid or not created!"
        );
        _;
    }

    modifier buyer_ready(uint256 receipt_number){
        require(transactions[receipt_number].buyer_ok == true);
        _;
    }

    modifier seller_ready(uint256 receipt_number){
        require(transactions[receipt_number].seller_ok == true);
        _;
    }

    // VARIABLES
    uint256 num_transactions;
    address admin;
    mapping (uint256 => Transaction) transactions;

    // FUNCTIONS
    constructor () {
        admin = msg.sender;
    }
    
    // Create a new transaction so people can push more
    // items onto the receipt
    function create_transaction (
        /**ARGUMENTS**/
        uint256 receipt_num
    )
        public
        returns (bool) 
    {
        // Create a new transaction and set the state to created
        num_transactions++;
        transactions[receipt_num].state = TransactionState.Created;
        // Push a creation date for the transaction
        transactions[receipt_num].dates[0] = block.timestamp;
        // Emit an event for new transaction being created
        emit TransactionCreated (receipt_num);
        return true;
    }

    // Function to add items to a transaction
    // Updates the list of items in receipt
    // Updates the total price of items for final payment
    function add_items_to_transaction(
        /**ARGUMENTS**/
        uint256 receipt_num,
        uint256[] memory item_ids,
        uint256[] memory item_prices
    )
        public
        transaction_created(receipt_num)
        returns (bool)
    {
        require (item_ids.length == item_prices.length, "Item IDs and Item Prices Don't Match!");

        // Push every item id into the receipt for payment
        for (uint i = 0; i < item_ids.length; i++){
            transactions[receipt_num].items.push(item_ids[i]);
        }

        // Add total using prices for clothes
        for (uint i = 0; i < item_prices.length; i++){
            transactions[receipt_num].total += item_prices[i];
        }

        // Emit an event with new total
        emit TransactionUpdated(
            receipt_num,
            transactions[receipt_num].total
        );

        return true;
    }

    function confirm_seller(
        /**ARGUMENTS**/
        uint256 receipt_num
    )
        public
        transaction_created(receipt_num)
        returns (bool)
    {
        // Seller says the transaction is ready to be reviewed by the buyer
        transactions[receipt_num].seller_ok = true;

        // emit event with seller agreement
        emit SellerOk(receipt_num, transactions[receipt_num].total);

        return true;
    }

    function confirm_buyer(
        /**ARGUMENTS**/
        uint256 receipt_num
    )
        public
        transaction_created(receipt_num)
        seller_ready(receipt_num)
        returns (bool)
    {
        // Buyer says the transaction is ready to be processed
        transactions[receipt_num].buyer_ok = true;

        // emit event with buyer agreement
        emit BuyerOk(receipt_num, transactions[receipt_num].total);

        return true;
    }

    // A function to let the buyer pay the amount owed in receipt
    // to the seller
    function pay_transaction(
        /**ARGUMENTS**/
        uint256 receipt_num
    )
        public
        transaction_payable(receipt_num)
        seller_ready(receipt_num)
        buyer_ready(receipt_num)
        returns (bool)
    {
        // Set transaction state to completed
        // Note: Should have an if/else statement to set transaction 
        // state to completed or failed.
        transactions[receipt_num].state = TransactionState.Completed;
        // Add payment completion date to transaction
        transactions[receipt_num].dates[1] = block.timestamp;
        // Emit event to begin funds transfer via bitcoin transaction
        emit PaymentInitiated(
            receipt_num,
            transactions[receipt_num].total
        );
        return true;
    }

    // Excuting a transaction to reverse the payment that was done due to
    // returning an item by a customer.
    function refund_transaction(
        /**ARGUMENTS**/
        uint256 receipt_num
    )
        public
        transaction_completed(receipt_num)
        returns (bool)
    {
        // Set transaction state to refunded
        transactions[receipt_num].state = TransactionState.Refunded;
        // Set refund date into transaction
        transactions[receipt_num].dates[2] = block.timestamp;
        // Emit an event to refund the transaction
        emit TransactionRefunded(
            receipt_num,
            transactions[receipt_num].total
        );
        return true;
    }

    // A function to get the state of the transaction
    function get_state(
        /**ARGUMENTS**/
        uint256 receipt_num
    )
        public
        view
        returns (TransactionState)
    {
        return transactions[receipt_num].state;
    }

    // A function to get the total number of transactions
    // done.
    function get_num_trans(
        /**ARGUMENTS**/
    )
        public
        view
        returns (uint256)
    {
        return num_transactions;
    }
}