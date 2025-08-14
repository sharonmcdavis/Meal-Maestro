package com.farmersmarket;

import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

// Stand class
class Stand {
    private Farmer farmer;
    private List<Produce> produceList;

    public Stand() {
        this.produceList = new ArrayList<>();
    }

    public void setFarmer(Farmer farmer) {
        this.farmer = farmer;
    }

    public Farmer getFarmer() {
        return farmer;
    }

    public void addProduce(Produce produce) {
        produceList.add(produce);
    }

    public List<Produce> getProduceList() {
        return produceList;
    }

    public void reduceProduceQuantity(String produceName, int amount) {
        for (Produce produce : produceList) {
            if (produce.getName().equalsIgnoreCase(produceName)) {
                produce.reduceQuantity(amount);
                return;
            }
        }
        System.out.println("Produce not found!");
    }

    @Override
    public String toString() {
        return "Farmer: " + farmer + ", Produce: " + produceList;
    }
}