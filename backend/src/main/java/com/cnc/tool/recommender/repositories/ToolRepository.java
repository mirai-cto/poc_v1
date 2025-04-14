package com.cnc.tool.recommender.repositories;

import com.cnc.tool.recommender.models.Tool;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface ToolRepository extends JpaRepository<Tool, Integer> {
} 