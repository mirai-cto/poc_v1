package com.cnc.tool.recommender.controllers;

import com.cnc.tool.recommender.models.CADFile;
import com.cnc.tool.recommender.repositories.CADFileRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/cad-files")
public class CADFileController {

    @Autowired
    private CADFileRepository cadFileRepository;

    @Value("${upload.dir:./uploads}")
    private String uploadDir;

    @GetMapping
    public ResponseEntity<List<CADFile>> getAllCADFiles() {
        return ResponseEntity.ok(cadFileRepository.findAll());
    }

    @GetMapping("/{id}")
    public ResponseEntity<CADFile> getCADFileById(@PathVariable Integer id) {
        return cadFileRepository.findById(id)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }

    @PostMapping
    public ResponseEntity<Map<String, Object>> uploadCADFile(@RequestParam("file") MultipartFile file) {
        try {
            // Create upload directory if it doesn't exist
            File directory = new File(uploadDir);
            if (!directory.exists()) {
                directory.mkdirs();
            }

            // Get original filename and extension
            String originalFilename = file.getOriginalFilename();
            String extension = "";
            if (originalFilename != null && originalFilename.contains(".")) {
                extension = originalFilename.substring(originalFilename.lastIndexOf(".") + 1);
            }

            // Check if file is a supported CAD format
            if (!extension.equalsIgnoreCase("stp") && !extension.equalsIgnoreCase("step")) {
                Map<String, Object> response = new HashMap<>();
                response.put("error", "Unsupported file format. Only .stp or .step files are supported.");
                return ResponseEntity.badRequest().body(response);
            }

            // Create unique filename to avoid conflicts
            String uniqueFilename = System.currentTimeMillis() + "_" + originalFilename;
            Path filePath = Paths.get(uploadDir, uniqueFilename);

            // Save file to disk
            Files.copy(file.getInputStream(), filePath);

            // Create and save CADFile entity
            CADFile cadFile = new CADFile();
            cadFile.setFilename(originalFilename);
            cadFile.setFilePath(filePath.toString());
            cadFile.setFileSize(file.getSize());
            cadFile.setFileFormat(extension);
            cadFile.setParsed(false);

            CADFile savedFile = cadFileRepository.save(cadFile);

            // Prepare response
            Map<String, Object> response = new HashMap<>();
            response.put("fileId", savedFile.getId());
            response.put("filename", savedFile.getFilename());
            response.put("message", "File uploaded successfully");

            return ResponseEntity.ok(response);

        } catch (IOException e) {
            Map<String, Object> response = new HashMap<>();
            response.put("error", "Failed to upload file: " + e.getMessage());
            return ResponseEntity.internalServerError().body(response);
        }
    }
} 