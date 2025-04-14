package com.cnc.tool.recommender.controllers;

import com.cnc.tool.recommender.models.Tool;
import com.cnc.tool.recommender.repositories.ToolRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/tools")
public class ToolController {

    @Autowired
    private ToolRepository toolRepository;

    @GetMapping
    public ResponseEntity<List<Tool>> getAllTools() {
        return ResponseEntity.ok(toolRepository.findAll());
    }

    @GetMapping("/{id}")
    public ResponseEntity<Tool> getToolById(@PathVariable Integer id) {
        return toolRepository.findById(id)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }
} 