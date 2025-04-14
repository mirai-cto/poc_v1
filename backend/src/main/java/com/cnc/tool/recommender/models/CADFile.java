package com.cnc.tool.recommender.models;

import lombok.Data;

import javax.persistence.*;
import java.time.LocalDateTime;

@Data
@Entity
@Table(name = "cad_files")
public class CADFile {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    @Column(name = "filename", nullable = false)
    private String filename;

    @Column(name = "file_path", nullable = false)
    private String filePath;

    @Column(name = "upload_date")
    private LocalDateTime uploadDate;

    @Column(name = "file_size")
    private Long fileSize;

    @Column(name = "file_format")
    private String fileFormat;

    @Column(name = "parsed")
    private Boolean parsed = false;

    @Column(name = "parsed_data_path")
    private String parsedDataPath;

    @PrePersist
    protected void onCreate() {
        uploadDate = LocalDateTime.now();
    }
} 