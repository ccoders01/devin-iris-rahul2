package com.mrm.modelregistry.repository;

import com.mrm.modelregistry.entity.Model;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface ModelRepository extends JpaRepository<Model, Long> {
    
    @Query("SELECT m FROM Model m WHERE " +
           "LOWER(m.modelName) LIKE LOWER(CONCAT('%', :searchTerm, '%')) OR " +
           "LOWER(m.modelVersion) LIKE LOWER(CONCAT('%', :searchTerm, '%')) OR " +
           "LOWER(m.modelSponsor) LIKE LOWER(CONCAT('%', :searchTerm, '%')) OR " +
           "LOWER(m.businessLine.displayName) LIKE LOWER(CONCAT('%', :searchTerm, '%')) OR " +
           "LOWER(m.modelType.displayName) LIKE LOWER(CONCAT('%', :searchTerm, '%')) OR " +
           "LOWER(m.riskRating.displayName) LIKE LOWER(CONCAT('%', :searchTerm, '%')) OR " +
           "LOWER(m.status.displayName) LIKE LOWER(CONCAT('%', :searchTerm, '%')) OR " +
           "CAST(m.id AS string) LIKE CONCAT('%', :searchTerm, '%')")
    List<Model> findBySearchTerm(@Param("searchTerm") String searchTerm);
}
