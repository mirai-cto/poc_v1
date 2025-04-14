package com.cnc.tool.recommender.controllers;

import com.cnc.tool.recommender.models.Machine;
import com.cnc.tool.recommender.repositories.MachineRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/machines")
public class MachineController {

    @Autowired
    private MachineRepository machineRepository;

    @GetMapping
    public ResponseEntity<List<Machine>> getAllMachines() {
        return ResponseEntity.ok(machineRepository.findAll());
    }

    @GetMapping("/{id}")
    public ResponseEntity<Machine> getMachineById(@PathVariable Integer id) {
        return machineRepository.findById(id)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }
} 