package com.farmersmarket;

import java.util.ArrayList;
import java.util.List;

// FarmersMarket class
public class FarmersMarket {
    private List<Stand> stands;
    private List<Farmer> farmers; // Global list of farmers

    public FarmersMarket() {
        this.stands = new ArrayList<>();
        this.farmers = new ArrayList<>(); // Initialize the farmer list
    }

    public void addStand(Stand stand) {
        stands.add(stand);
    }

    public List<Stand> getStands() {
        return stands;
    }

    public void addFarmer(Farmer farmer) {
        farmers.add(farmer); // Add farmer to the global list
    }

    public List<Farmer> getFarmers() {
        return farmers; // Return the list of all farmers
    }

    public void searchProduce(String produceName) {
        boolean found = false;
        for (Stand stand : stands) {
            for (Produce produce : stand.getProduceList()) {
                if (produce.getName().equalsIgnoreCase(produceName) && produce.getQuantity() > 0) {
                    System.out.println("Found " + produceName + " at " + stand.getFarmer() + "'s stand. Quantity: " + produce.getQuantity());
                    found = true;
                }
            }
        }
        if (!found) {
            System.out.println("Produce not found!");
        }
    }

    public void buyProduce(String produceName, int amount) {
        for (Stand stand : stands) {
            for (Produce produce : stand.getProduceList()) {
                if (produce.getName().equalsIgnoreCase(produceName) && produce.getQuantity() >= amount) {
                    stand.reduceProduceQuantity(produceName, amount);
                    System.out.println("Bought " + amount + " of " + produceName + " from " + stand.getFarmer() + "'s stand.");
                    return;
                }
            }
        }
        System.out.println("Produce not available in sufficient quantity!");
    }

}