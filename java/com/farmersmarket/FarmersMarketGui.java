package com.farmersmarket;

import javax.swing.*;
import java.awt.*;
import java.util.ArrayList;
import java.util.List;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;

public class FarmersMarketGui {
    private static FarmersMarket market;
    private static List<Farmer> farmers; // Global list of farmers
    private static List<Stand> stands; // Global list of stands
    private static JFrame frame = new JFrame("Farmer's Market");

    public FarmersMarketGui() {
        // market = new FarmersMarket(); // Initialize the FarmersMarket object
        // farmers = new ArrayList<>(); // Initialize the farmer list
        // stands = new ArrayList<>(); // Initialize the stand list
        // createAndShowGui();
    }

    public static void main(String[] args) {
        market = new FarmersMarket(); // Initialize the FarmersMarket object
        farmers = new ArrayList<>(); // Initialize the farmer list
        stands = new ArrayList<>(); // Initialize the stand list
        loadDataFromFile("setupData.txt"); // Load data from file
        createAndShowGui();
        //SwingUtilities.invokeLater(FarmersMarketGui::new);
    }

    private static void loadDataFromFile(String filePath) {
       // Print the absolute path of the file for debugging
        File file = new File(filePath);
        System.out.println("Loading data from file: " + file.getAbsolutePath());

        try (BufferedReader reader = new BufferedReader(new FileReader(filePath))) {
            String line;
            while ((line = reader.readLine()) != null) {
                line = line.trim();
                if (line.isEmpty() || line.startsWith("#")) {
                    continue; // Skip empty lines and comments
                }
    
                if (line.startsWith("Farmer:")) {
                    // Parse farmer
                    String farmerName = line.substring(7).trim();
                    Farmer farmer = new Farmer(farmerName);
                    market.addFarmer(farmer);
                } else if (line.startsWith("Stand:")) {
                    // Parse stand
                    String[] parts = line.substring(6).split(",");
                    if (parts.length == 2) {
                        String standName = parts[0].trim();
                        String farmerName = parts[1].trim();
                        Farmer farmer = market.getFarmers().stream()
                                .filter(f -> f.getName().equalsIgnoreCase(farmerName))
                                .findFirst()
                                .orElse(null);
                        if (farmer != null) {
                            Stand stand = new Stand();
                            stand.setFarmer(farmer);
                            market.addStand(stand);
                        }
                    }
                } else if (line.startsWith("Produce:")) {
                    // Parse produce
                    String[] parts = line.substring(8).split(",");
                    if (parts.length == 3) {
                        String produceName = parts[0].trim();
                        int quantity = Integer.parseInt(parts[1].trim());
                        String standName = parts[2].trim();
                        Stand stand = market.getStands().stream()
                                .filter(s -> s.toString().contains(standName))
                                .findFirst()
                                .orElse(null);
                        if (stand != null) {
                            Produce produce = new Produce(produceName, quantity);
                            stand.addProduce(produce);
                        }
                    }
                }
            }
        } catch (IOException e) {
            JOptionPane.showMessageDialog(frame, "Error reading data file: " + e.getMessage());
        } catch (NumberFormatException e) {
            JOptionPane.showMessageDialog(frame, "Invalid number format in data file: " + e.getMessage());
        }
    }

    private static void createAndShowGui() {
        // Create the main frame
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setSize(600, 400);

        // Create a panel for buttons
        JPanel buttonPanel = new JPanel();
        // Create a vertical layout for the button panel
        buttonPanel.setLayout(new BoxLayout(buttonPanel, BoxLayout.Y_AXIS));

        // Create buttons with numbering
        JButton createFarmerButton = new JButton("Create Farmer");
        JButton createStandButton = new JButton("Create Stand");
        JButton addProduceButton = new JButton("Add Produce");
        JButton displayStandsButton = new JButton("Display Stands");
        JButton searchProduceButton = new JButton("Search Produce");
        JButton buyProduceButton = new JButton("Buy Produce");
        JButton exitButton = new JButton("Exit");

        // Add buttons to the panel
        buttonPanel.add(createFarmerButton);
        buttonPanel.add(Box.createVerticalStrut(10)); // Add spacing between buttons
        buttonPanel.add(createStandButton);
        buttonPanel.add(Box.createVerticalStrut(10));
        buttonPanel.add(addProduceButton);
        buttonPanel.add(Box.createVerticalStrut(10));
        buttonPanel.add(displayStandsButton);
        buttonPanel.add(Box.createVerticalStrut(10));
        buttonPanel.add(searchProduceButton);
        buttonPanel.add(Box.createVerticalStrut(10));
        buttonPanel.add(buyProduceButton);
        buttonPanel.add(Box.createVerticalStrut(10));
        buttonPanel.add(exitButton);

        // Create a text area for displaying results
        JTextArea outputArea = new JTextArea();
        outputArea.setEditable(false);
        JScrollPane scrollPane = new JScrollPane(outputArea);

        // Add action listener for the Exit button
        exitButton.addActionListener(e -> {
            int confirm = JOptionPane.showConfirmDialog(
                frame,
                "Are you sure you want to exit?",
                "Exit Confirmation",
                JOptionPane.YES_NO_OPTION
            );
            if (confirm == JOptionPane.YES_OPTION) {
                System.exit(0); // Exit the application
            }
        });

        // Add action listeners to buttons
        createFarmerButton.addActionListener(e -> {
            String farmerName = JOptionPane.showInputDialog(frame, "Enter Farmer's Name:");
            if (farmerName != null && !farmerName.trim().isEmpty()) {
                Farmer farmer = new Farmer(farmerName);
                farmers.add(farmer); // Add farmer to the global list
                JOptionPane.showMessageDialog(frame, "Farmer " + farmerName + " created!");
            }
        });

    createStandButton.addActionListener(e -> {
        // Prompt for stand name
        String standName = JOptionPane.showInputDialog(frame, "Enter Stand Name:");
        if (standName == null || standName.trim().isEmpty()) {
            JOptionPane.showMessageDialog(frame, "Stand name cannot be empty!");
            return;
        }

        // Check if there are any farmers available
        // List<Farmer> farmers = new ArrayList<>();
        for (Stand stand : market.getStands()) {
            if (stand.getFarmer() != null) {
                farmers.add(stand.getFarmer());
            }
        }

        if (farmers.isEmpty()) {
            JOptionPane.showMessageDialog(frame, "No farmers available. Create a farmer first.");
            return;
        }

        // Let the user select a farmer
        Farmer[] farmerArray = farmers.toArray(new Farmer[0]);
        Farmer selectedFarmer = (Farmer) JOptionPane.showInputDialog(
            frame,
            "Select a Farmer for the Stand:",
            "Assign Farmer",
            JOptionPane.PLAIN_MESSAGE,
            null,
            farmerArray,
            farmerArray[0]
        );

        if (selectedFarmer == null) {
            JOptionPane.showMessageDialog(frame, "No farmer selected. Stand creation canceled.");
            return;
        }

        // Create the stand and assign the farmer
        Stand stand = new Stand();
        stand.setFarmer(selectedFarmer);
        market.addStand(stand);
        JOptionPane.showMessageDialog(frame, "Stand '" + standName + "' created and assigned to Farmer " + selectedFarmer.getName() + "!");
    });

    addProduceButton.addActionListener(e -> {
        if (market.getStands().isEmpty()) {
            JOptionPane.showMessageDialog(frame, "No stands available. Create a stand first.");
            return;
        }
    
        // Let the user select a stand
        Stand[] standArray = market.getStands().toArray(new Stand[0]);
        Stand selectedStand = (Stand) JOptionPane.showInputDialog(
            frame,
            "Select a Stand to Add Produce:",
            "Select Stand",
            JOptionPane.PLAIN_MESSAGE,
            null,
            standArray,
            standArray[0]
        );
    
        if (selectedStand == null) {
            JOptionPane.showMessageDialog(frame, "No stand selected. Operation canceled.");
            return;
        }
    
        // Prompt for produce details
        String produceName = JOptionPane.showInputDialog(frame, "Enter Produce Name:");
        if (produceName == null || produceName.trim().isEmpty()) {
            JOptionPane.showMessageDialog(frame, "Produce name cannot be empty!");
            return;
        }
    
        String quantityStr = JOptionPane.showInputDialog(frame, "Enter Quantity:");
        try {
            int quantity = Integer.parseInt(quantityStr);
            Produce produce = new Produce(produceName, quantity);
            selectedStand.addProduce(produce); // Add produce to the selected stand
            JOptionPane.showMessageDialog(frame, produceName + " added to the stand!");
        } catch (NumberFormatException ex) {
            JOptionPane.showMessageDialog(frame, "Invalid quantity!");
        }
    });
        
    displayStandsButton.addActionListener(e -> {
            StringBuilder display = new StringBuilder();
            for (Stand stand : market.getStands()) {
                display.append(stand).append("\n");
            }
            outputArea.setText(display.toString());
        });

        searchProduceButton.addActionListener(e -> {
            String produceName = JOptionPane.showInputDialog(frame, "Enter Produce Name to Search:");
            if (produceName != null && !produceName.trim().isEmpty()) {
                StringBuilder results = new StringBuilder();
                for (Stand stand : market.getStands()) {
                    for (Produce produce : stand.getProduceList()) {
                        if (produce.getName().equalsIgnoreCase(produceName)) {
                            results.append("Found ").append(produceName)
                                    .append(" at ").append(stand.getFarmer())
                                    .append("'s stand. Quantity: ").append(produce.getQuantity()).append("\n");
                        }
                    }
                }
                if (results.length() == 0) {
                    results.append("Produce not found!");
                }
                outputArea.setText(results.toString());
            }
        });

        buyProduceButton.addActionListener(e -> {
            String produceName = JOptionPane.showInputDialog(frame, "Enter Produce Name to Buy:");
            String quantityStr = JOptionPane.showInputDialog(frame, "Enter Quantity to Buy:");
            try {
                int quantity = Integer.parseInt(quantityStr);
                market.buyProduce(produceName, quantity);
                JOptionPane.showMessageDialog(frame, "Bought " + quantity + " of " + produceName + "!");
            } catch (NumberFormatException ex) {
                JOptionPane.showMessageDialog(frame, "Invalid quantity!");
            }
        });

        // Add components to the frame
        frame.setLayout(new BorderLayout());
        frame.add(buttonPanel, BorderLayout.NORTH);
        frame.add(scrollPane, BorderLayout.CENTER);

        // Show the frame
        frame.setVisible(true);
    }
}