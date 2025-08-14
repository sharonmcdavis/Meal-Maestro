package com.farmersmarket;

// Produce class
class Produce {
    private String name;
    private int quantity;

    public Produce(String name, int quantity) {
        this.name = name;
        this.quantity = quantity;
    }

    public String getName() {
        return name;
    }

    public int getQuantity() {
        return quantity;
    }

    public void reduceQuantity(int amount) {
        if (amount <= quantity) {
            quantity -= amount;
        } else {
            System.out.println("Not enough stock available!");
        }
    }

    @Override
    public String toString() {
        return name + " (Quantity: " + quantity + ")";
    }
}