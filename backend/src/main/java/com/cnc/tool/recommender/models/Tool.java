package com.cnc.tool.recommender.models;

import lombok.Data;

import javax.persistence.*;
import java.math.BigDecimal;
import java.time.LocalDateTime;

@Data
@Entity
@Table(name = "tools")
public class Tool {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    @Column(name = "name", nullable = false)
    private String name;

    @Column(name = "type", nullable = false)
    private String type;

    @Column(name = "material")
    private String material;

    @Column(name = "diameter")
    private BigDecimal diameter;

    @Column(name = "flute_count")
    private Integer fluteCount;

    @Column(name = "overall_length")
    private BigDecimal overallLength;

    @Column(name = "cutting_length")
    private BigDecimal cuttingLength;

    @Column(name = "shank_diameter")
    private BigDecimal shankDiameter;

    @Column(name = "max_doc")
    private BigDecimal maxDepthOfCut;

    @Column(name = "max_rpm")
    private Integer maxRpm;

    @Column(name = "manufacturer")
    private String manufacturer;

    @Column(name = "created_at")
    private LocalDateTime createdAt;

    @Column(name = "updated_at")
    private LocalDateTime updatedAt;

    @PrePersist
    protected void onCreate() {
        createdAt = LocalDateTime.now();
        updatedAt = LocalDateTime.now();
    }

    @PreUpdate
    protected void onUpdate() {
        updatedAt = LocalDateTime.now();
    }
} 