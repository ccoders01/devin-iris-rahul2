package com.mrm.modelregistry.repository;

import com.mrm.modelregistry.entity.ModelTypeEntity;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import java.util.Optional;

@Repository
public interface ModelTypeRepository extends JpaRepository<ModelTypeEntity, Long> {
    Optional<ModelTypeEntity> findByCode(String code);
}
