package com.mrm.modelregistry.repository;

import com.mrm.modelregistry.entity.BusinessLineEntity;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import java.util.Optional;

@Repository
public interface BusinessLineRepository extends JpaRepository<BusinessLineEntity, Long> {
    Optional<BusinessLineEntity> findByCode(String code);
}
