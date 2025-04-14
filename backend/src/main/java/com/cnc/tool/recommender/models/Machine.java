package com.cnc.tool.recommender.models;

import lombok.Data;

import javax.persistence.*;
import java.math.BigDecimal;
import java.time.LocalDateTime;

@Data
@Entity
@Table(name = "machines")
public class Machine {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    @Column(name = "name", nullable = false)
    private String name;

    @Column(name = "model")
    private String model;

    @Column(name = "manufacturer")
    private String manufacturer;

    @Column(name = "max_rpm")
    private Integer maxRpm;

    @Column(name = "max_feed_rate")
    private BigDecimal maxFeedRate;

    @Column(name = "spindle_power")
    private BigDecimal spindlePower;

    @Column(name = "max_tool_diameter")
    private BigDecimal maxToolDiameter;

    @Column(name = "min_tool_diameter")
    private BigDecimal minToolDiameter;

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