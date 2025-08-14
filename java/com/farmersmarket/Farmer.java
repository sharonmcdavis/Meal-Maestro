package com.farmersmarket;

// Farmer class
class Farmer {
    private String name;

    public Farmer(String name) {
        this.name = name;
    }

    public String getName() {
        return name;
    }

    @Override
    public String toString() {
        return name;
    }
}
