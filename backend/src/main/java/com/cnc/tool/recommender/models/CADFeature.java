package com.cnc.tool.recommender.models;

import lombok.Data;

import javax.persistence.*;
import java.math.BigDecimal;
import java.time.LocalDateTime;

@Data
@Entity
@Table(name = "cad_features")
public class CADFeature {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    @ManyToOne
    @JoinColumn(name = "cad_file_id", nullable = false)
    private CADFile cadFile;

    @Column(name = "feature_name")
    private String featureName;

    @Column(name = "x_position")
    private BigDecimal xPosition;

    @Column(name = "y_position")
    private BigDecimal yPosition;

    @Column(name = "z_position")
    private BigDecimal zPosition;

    @Column(name = "width")
    private BigDecimal width;

    @Column(name = "height")
    private BigDecimal height;

    @Column(name = "depth")
    private BigDecimal depth;

    @Column(name = "radius")
    private BigDecimal radius;

    @Column(name = "angle")
    private BigDecimal angle;

    @Column(name = "created_at")
    private LocalDateTime createdAt;

    @PrePersist
    protected void onCreate() {
        createdAt = LocalDateTime.now();
    }
} 