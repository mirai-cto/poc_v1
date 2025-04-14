package com.cnc.tool.recommender.repositories;

import com.cnc.tool.recommender.models.CADFile;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface CADFileRepository extends JpaRepository<CADFile, Integer> {
} 