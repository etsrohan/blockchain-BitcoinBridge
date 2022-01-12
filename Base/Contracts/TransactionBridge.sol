// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

contract TransactionBridge {
    // ENUMS
    enum TransactionState {NotCreated, Created, Completed, Failed, Refunded}

    // STRUCTS
    struct Transaction {
        TransactionState state;
        uint256[] items;
        uint256 receipt_num;
        uint256 total;             // Amount Due/Paid/Refunded in cents
        uint256[3] dates;          // Creation, Completion, Refund Dates in epoch time.
    }

    // EVENTS
    event TransactionCreated (uint256 indexed transaction_id, uint256 receipt_number);
    event TransactionUpdated (uint256 indexed transaction_id, uint256 receipt_number, uint256 total);

    // MODIFIERS
    modifier transaction_created(uint256 transaction_id){
        require(transactions[transaction_id].state == TransactionState.Created, "Transaction Not Created!");
        _;
    }

    modifier transaction_completed(uint256 transaction_id){
        require(transactions[transaction_id].state == TransactionState.Completed, "Transaction Not Completed!");
        _;
    }

    modifier transaction_payable(uint256 transaction_id){
        require(
            transactions[transaction_id].state == TransactionState.Created ||
            transactions[transaction_id].state == TransactionState.Failed,
            "Transaction already paid or not created!"
        );
        _;
    }

    // VARIABLES
    uint256 num_transactions;
    mapping (uint256 => Transaction) transactions;

    // FUNCTIONS

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
        uint256 trans_id = num_transactions++;
        transactions[trans_id].state = TransactionState.Created;
        // Attach a receipt number to the transaction
        transactions[trans_id].receipt_num = receipt_num;
        // Push a creation date for the transaction
        transactions[trans_id].dates[0] = block.timestamp;
        // Emit an event for new transaction being created
        emit TransactionCreated (trans_id, receipt_num);
        return true;
    }

    // Function to add items to a transaction
    // Updates the list of items in receipt
    // Updates the total price of items for final payment
    function add_items_to_transaction(
        /**ARGUMENTS**/
        uint256 trans_id,
        uint256[] memory item_ids,
        uint256[] memory item_prices
    )
        public
        transaction_created(trans_id)
        returns (bool)
    {
        require (item_ids.length == item_prices.length, "Item IDs and Item Prices Don't Match!");

        // Push every item id into the receipt for payment
        for (uint i = 0; i < item_ids.length; i++){
            transactions[trans_id].items.push(item_ids[i]);
        }

        // Add total using prices for clothes
        for (uint i = 0; i < item_prices.length; i++){
            transactions[trans_id].total += item_prices[i];
        }

        // Emit an event with new total
        emit TransactionUpdated(
            trans_id,
            transactions[trans_id].receipt_num,
            transactions[trans_id].total
        );

        return true;
    }

    // A function to let the buyer pay the amount owed in receipt
    // to the seller
    function pay_transaction(
        /**ARGUMENTS**/
        uint256 trans_id
    )
        public
        transaction_payable(trans_id)
        returns (bool)
    {
        // Add stuff to interact with a bitcoin chain

        // Set transaction state to completed
        // Should have an if/else statement to set transaction 
        // state to completed or failed.
        transactions[trans_id].state = TransactionState.Completed;
        return true;
    }

    // 
    function refund_transaction(
        /**ARGUMENTS**/
        uint256 trans_id
    )
        public
        transaction_completed(trans_id)
        returns (bool)
    {
        // Add stuff to interact with bitcoin chain

        // Set transaction state to refunded
        transactions[trans_id].state = TransactionState.Refunded;
        return true;
    }
}