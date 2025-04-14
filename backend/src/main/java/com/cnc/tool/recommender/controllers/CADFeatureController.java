package com.cnc.tool.recommender.controllers;

import com.cnc.tool.recommender.models.CADFeature;
import com.cnc.tool.recommender.models.CADFile;
import com.cnc.tool.recommender.repositories.CADFeatureRepository;
import com.cnc.tool.recommender.repositories.CADFileRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestTemplate;

import java.io.File;
import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/cad-files/{fileId}/features")
public class CADFeatureController {

    @Autowired
    private CADFeatureRepository cadFeatureRepository;

    @Autowired
    private CADFileRepository cadFileRepository;

    @Value("${ml.module.url}")
    private String mlModuleUrl;

    @GetMapping
    public ResponseEntity<?> getFeatures(@PathVariable Integer fileId) {
        // Check if file exists
        CADFile cadFile = cadFileRepository.findById(fileId).orElse(null);
        if (cadFile == null) {
            Map<String, String> response = new HashMap<>();
            response.put("error", "CAD file not found");
            return ResponseEntity.notFound().build();
        }

        // Check if features already exist
        List<CADFeature> existingFeatures = cadFeatureRepository.findByCadFileId(fileId);
        if (!existingFeatures.isEmpty()) {
            return ResponseEntity.ok(existingFeatures);
        }

        // Check if the file exists on disk
        File file = new File(cadFile.getFilePath());
        if (!file.exists()) {
            Map<String, String> response = new HashMap<>();
            response.put("error", "File not found on disk");
            return ResponseEntity.notFound().build();
        }

        // In a real implementation, we would call the ML module to extract features
        // For this demo, we'll create mock features
        try {
            // Sample mock data - in a real implementation, we'd call the ML module
            List<CADFeature> mockFeatures = createMockFeatures(cadFile);
            
            // Save mock features to database
            cadFeatureRepository.saveAll(mockFeatures);
            
            // Update CAD file to mark as parsed
            cadFile.setParsed(true);
            cadFileRepository.save(cadFile);
            
            return ResponseEntity.ok(mockFeatures);
        } catch (Exception e) {
            Map<String, String> response = new HashMap<>();
            response.put("error", "Failed to extract features: " + e.getMessage());
            return ResponseEntity.internalServerError().body(response);
        }
    }

    private List<CADFeature> createMockFeatures(CADFile cadFile) {
        List<CADFeature> features = new ArrayList<>();
        
        // Mock hole feature
        CADFeature hole = new CADFeature();
        hole.setCadFile(cadFile);
        hole.setFeatureName("Hole");
        hole.setXPosition(new BigDecimal("10.0"));
        hole.setYPosition(new BigDecimal("20.0"));
        hole.setZPosition(new BigDecimal("0.0"));
        hole.setRadius(new BigDecimal("5.0"));
        hole.setDepth(new BigDecimal("15.0"));
        features.add(hole);
        
        // Mock pocket feature
        CADFeature pocket = new CADFeature();
        pocket.setCadFile(cadFile);
        pocket.setFeatureName("Pocket");
        pocket.setXPosition(new BigDecimal("50.0"));
        pocket.setYPosition(new BigDecimal("60.0"));
        pocket.setZPosition(new BigDecimal("0.0"));
        pocket.setWidth(new BigDecimal("30.0"));
        pocket.setHeight(new BigDecimal("20.0"));
        pocket.setDepth(new BigDecimal("10.0"));
        features.add(pocket);
        
        // Mock slot feature
        CADFeature slot = new CADFeature();
        slot.setCadFile(cadFile);
        slot.setFeatureName("Slot");
        slot.setXPosition(new BigDecimal("100.0"));
        slot.setYPosition(new BigDecimal("80.0"));
        slot.setZPosition(new BigDecimal("0.0"));
        slot.setWidth(new BigDecimal("50.0"));
        slot.setHeight(new BigDecimal("8.0"));
        slot.setDepth(new BigDecimal("12.0"));
        features.add(slot);
        
        return features;
    }
} 