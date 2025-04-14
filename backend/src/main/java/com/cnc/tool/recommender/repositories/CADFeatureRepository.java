package com.cnc.tool.recommender.repositories;

import com.cnc.tool.recommender.models.CADFeature;
import com.cnc.tool.recommender.models.CADFile;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface CADFeatureRepository extends JpaRepository<CADFeature, Integer> {
    List<CADFeature> findByCadFile(CADFile cadFile);
    List<CADFeature> findByCadFileId(Integer cadFileId);
} 