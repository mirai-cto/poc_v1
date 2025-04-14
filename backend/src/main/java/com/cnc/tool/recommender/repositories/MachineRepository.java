package com.cnc.tool.recommender.repositories;

import com.cnc.tool.recommender.models.Machine;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface MachineRepository extends JpaRepository<Machine, Integer> {
} 