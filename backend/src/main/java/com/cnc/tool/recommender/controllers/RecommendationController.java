package com.cnc.tool.recommender.controllers;

import com.cnc.tool.recommender.models.CADFile;
import com.cnc.tool.recommender.models.Machine;
import com.cnc.tool.recommender.models.Tool;
import com.cnc.tool.recommender.repositories.CADFeatureRepository;
import com.cnc.tool.recommender.repositories.CADFileRepository;
import com.cnc.tool.recommender.repositories.MachineRepository;
import com.cnc.tool.recommender.repositories.ToolRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.math.BigDecimal;
import java.util.*;

@RestController
@RequestMapping("/recommendations")
public class RecommendationController {

    @Autowired
    private CADFileRepository cadFileRepository;

    @Autowired
    private MachineRepository machineRepository;
    
    @Autowired
    private ToolRepository toolRepository;
    
    @Autowired
    private CADFeatureRepository cadFeatureRepository;
    
    @PostMapping
    public ResponseEntity<?> generateRecommendations(
            @RequestParam Integer cadFileId,
            @RequestParam Integer machineId) {
        
        // Check if file exists
        CADFile cadFile = cadFileRepository.findById(cadFileId).orElse(null);
        if (cadFile == null) {
            Map<String, String> response = new HashMap<>();
            response.put("error", "CAD file not found");
            return ResponseEntity.notFound().build();
        }
        
        // Check if file has been parsed
        if (!cadFile.getParsed()) {
            Map<String, String> response = new HashMap<>();
            response.put("error", "CAD file has not been parsed yet");
            return ResponseEntity.badRequest().body(response);
        }
        
        // Check if machine exists
        Machine machine = machineRepository.findById(machineId).orElse(null);
        if (machine == null) {
            Map<String, String> response = new HashMap<>();
            response.put("error", "Machine not found");
            return ResponseEntity.notFound().build();
        }
        
        // In a real implementation, we would call a service to generate recommendations
        // based on the CAD features, machine constraints, and tool database
        // For this demo, we'll create mock recommendations
        List<Map<String, Object>> recommendations = generateMockRecommendations(cadFile, machine);
        
        return ResponseEntity.ok(recommendations);
    }
    
    @PostMapping("/{recommendationId}/feedback")
    public ResponseEntity<?> submitFeedback(
            @PathVariable String recommendationId,
            @RequestParam Integer rating,
            @RequestParam(required = false) String comments) {
        
        // Validate rating
        if (rating < 1 || rating > 5) {
            Map<String, String> response = new HashMap<>();
            response.put("error", "Rating must be between 1 and 5");
            return ResponseEntity.badRequest().body(response);
        }
        
        // In a real implementation, we would save the feedback to the database
        // For this demo, we'll just return a success message
        Map<String, Object> response = new HashMap<>();
        response.put("message", "Feedback submitted successfully");
        response.put("recommendationId", recommendationId);
        response.put("rating", rating);
        if (comments != null && !comments.isEmpty()) {
            response.put("comments", comments);
        }
        
        return ResponseEntity.ok(response);
    }
    
    private List<Map<String, Object>> generateMockRecommendations(CADFile cadFile, Machine machine) {
        List<Map<String, Object>> recommendations = new ArrayList<>();
        
        // Get all tools
        List<Tool> allTools = toolRepository.findAll();
        
        // Filter tools based on machine constraints
        List<Tool> compatibleTools = allTools.stream()
                .filter(tool -> {
                    // Check if tool diameter is within machine limits
                    if (tool.getDiameter().compareTo(machine.getMaxToolDiameter()) > 0 ||
                            tool.getDiameter().compareTo(machine.getMinToolDiameter()) < 0) {
                        return false;
                    }
                    
                    // Check if tool RPM is within machine limits
                    if (tool.getMaxRpm() != null && tool.getMaxRpm() > machine.getMaxRpm()) {
                        return false;
                    }
                    
                    return true;
                })
                .toList();
        
        // Mock recommendation for roughing
        Optional<Tool> roughingTool = compatibleTools.stream()
                .filter(tool -> "end_mill".equals(tool.getType()))
                .findFirst();
        
        if (roughingTool.isPresent()) {
            Map<String, Object> recommendation = new HashMap<>();
            recommendation.put("id", UUID.randomUUID().toString());
            recommendation.put("toolId", roughingTool.get().getId());
            recommendation.put("toolName", roughingTool.get().getName());
            recommendation.put("operation", "roughing");
            recommendation.put("speed", Math.min(roughingTool.get().getMaxRpm(), machine.getMaxRpm()));
            recommendation.put("feed", calculateFeed(roughingTool.get(), 0.05, machine.getMaxFeedRate()));
            recommendations.add(recommendation);
        }
        
        // Mock recommendation for finishing
        Optional<Tool> finishingTool = compatibleTools.stream()
                .filter(tool -> "ball_end_mill".equals(tool.getType()))
                .findFirst();
        
        if (finishingTool.isPresent()) {
            Map<String, Object> recommendation = new HashMap<>();
            recommendation.put("id", UUID.randomUUID().toString());
            recommendation.put("toolId", finishingTool.get().getId());
            recommendation.put("toolName", finishingTool.get().getName());
            recommendation.put("operation", "finishing");
            recommendation.put("speed", Math.min(finishingTool.get().getMaxRpm(), machine.getMaxRpm()));
            recommendation.put("feed", calculateFeed(finishingTool.get(), 0.03, machine.getMaxFeedRate()));
            recommendations.add(recommendation);
        }
        
        // Mock recommendation for drilling
        Optional<Tool> drillingTool = compatibleTools.stream()
                .filter(tool -> "drill".equals(tool.getType()))
                .findFirst();
        
        if (drillingTool.isPresent()) {
            Map<String, Object> recommendation = new HashMap<>();
            recommendation.put("id", UUID.randomUUID().toString());
            recommendation.put("toolId", drillingTool.get().getId());
            recommendation.put("toolName", drillingTool.get().getName());
            recommendation.put("operation", "drilling");
            recommendation.put("speed", Math.min(drillingTool.get().getMaxRpm(), machine.getMaxRpm()));
            recommendation.put("feed", calculateFeed(drillingTool.get(), 0.02, machine.getMaxFeedRate()));
            recommendations.add(recommendation);
        }
        
        return recommendations;
    }
    
    private double calculateFeed(Tool tool, double chipLoad, BigDecimal maxFeedRate) {
        // Basic feed rate calculation: feed = rpm * chipload * number of flutes
        int flutes = tool.getFluteCount() != null ? tool.getFluteCount() : 1;
        double feed = tool.getMaxRpm() * chipLoad * flutes;
        
        // Cap feed rate at machine maximum
        return Math.min(feed, maxFeedRate.doubleValue());
    }
} 